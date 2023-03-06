# Copyright (c) 2022 Intel Corporation
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# SPDX-License-Identifier: MIT

import requests
import json
import argparse
import time
import pandas as pd
import os
from flattening import (
    separating_col_func,
    explode_multiple,
    equivalent_col_func,
    flattening,
    intersection_cols,
)

cnvrg_workdir = os.environ.get("CNVRG_WORKDIR", "/cnvrg")

"""
This function is used to analyze the response returned from Monday
In case complexity budget is exhausted, we wait 60secs to query again
"""


def check_budget_error(returns, query, apiUrl, headers):
    try:

        returns = returns["data"]

    except KeyError:

        try:
            if "Complexity budget exhausted" in returns["error_message"]:
                print("going to wait 60sec because complexity budget exhausted")
                time.sleep(60)
                returns = caller(query, apiUrl, headers)
            else:
                raise Exception(returns)
        except KeyError:

            if "Not Authenticated" in returns["errors"][0]:
                print("*****YOUR API KEY IS NOT VALID********")
                raise Exception(returns)
            else:
                raise Exception(returns)
    return returns


"""
This function is used to make calls to the Monday API
"""


def caller(query, apiUrl, headers):
    data = {"query": query}
    r = requests.post(url=apiUrl, json=data, headers=headers)
    returns = r.json()
    returns = check_budget_error(returns, query, apiUrl, headers)
    return returns


"""
This function takes input a GraphQL query and saves the reponse as a json file.
"""


def specificquery(sq, apiUrl, headers):
    returns = caller(sq, apiUrl, headers)
    # save the json response
    json_object = json.dumps(returns, indent=4)
    with open(cnvrg_workdir + "/specific.json", "w") as outfile:
        outfile.write(json_object)


"""
This function creates two CSVs one for all workspaces and one for all boards contanining high level information 
and returns board ids
"""


def save_workspace_boards(apiUrl, headers):
    query = "{ boards { name id workspace {id name description kind} permissions owners{name}}}"

    returns = caller(query, apiUrl, headers)
    board_ids = []
    workspaces_id = {}
    df_workspace = pd.DataFrame(columns=["id", "name", "kind", "description"])
    df_boards = pd.DataFrame(
        columns=["board_id", "workspace_id", "name", "owners", "permissions"]
    )
    for i, board in enumerate(returns["boards"]):
        print("executing for board number: ", i + 1)
        board_ids.append(board["id"])
        owner_names = utility_flattendict(board["owners"], "name")
        if board["workspace"] == None:
            df_boards.loc[len(df_boards)] = [
                board["id"],
                None,
                board["name"],
                owner_names,
                board["permissions"],
            ]
        else:
            df_boards.loc[len(df_boards)] = [
                board["id"],
                board["workspace"]["id"],
                board["name"],
                owner_names,
                board["permissions"],
            ]

        try:
            workspaces_id[
                board["workspace"]["id"]
            ]  # check if we have already added an entry for this workspace
            pass
        except KeyError:
            ###write to csv for all workspaces
            df_workspace.loc[len(df_workspace)] = [
                board["workspace"]["id"],
                board["workspace"]["name"],
                board["workspace"]["kind"],
                board["workspace"]["description"],
            ]
            workspaces_id[board["workspace"]["id"]] = "entry added"
        except TypeError:  # if the workspace is None
            pass
    print("saving boards and workspaces")
    df_boards.to_csv(cnvrg_workdir + "/boards.csv")
    df_workspace.to_csv(cnvrg_workdir + "/workspaces.csv")
    return board_ids


"""
A helper function to convert a list of dictionary names to a list.
"""


def utility_flattendict(dictone, key):
    try:
        newlist = [item[key] for item in dictone]
        return newlist
    except:
        newlist = dictone
    return newlist


"""
This function creates one csv per board containing all the necessary data in the board
"""


def boards(boardids, args, apiUrl, headers):
    for everyboard in boardids:
        print("querying board id: " + everyboard)
        query = (
            "{ boards (ids:"
            + everyboard
            + ") {     items { id name subscribers {name} column_values { title text } subitems { name  }}}}"
        )
        returns = caller(query, apiUrl, headers)
        cols = ["item_id", "name", "subscribers", "subitems_name"]
        try:
            for col in returns["boards"][0]["items"][0]["column_values"]:
                cols.append(col["title"])
        except IndexError:  # it means there are no items in this board, so will skip creating a csv for this board
            pass
        df = pd.DataFrame(columns=cols)
        writer = []
        for item in returns["boards"][0]["items"]:
            # go through subscriber names
            subsnames = utility_flattendict(item["subscribers"], "name")
            # go through subitems names
            subitemnames = utility_flattendict(item["subitems"], "name")
            writer.extend([item["id"], item["name"], subsnames, subitemnames])
            for colvalue in item["column_values"]:
                writer.append(colvalue["text"])
            df.loc[len(df)] = writer
            writer = []

        df = check_flatten_csv(args, df)
        print("saving board id: " + everyboard)
        df.to_csv(cnvrg_workdir + "/" + everyboard + ".csv")


"""
This function is used to check if user wants to flatten the csv
"""


def check_flatten_csv(args, df):
    if args.equivalent_columns == "None" or args.separation_columns == "None":
        pass
    else:
        sep_cols_task = intersection_cols(df, args.separation_columns)
        if sep_cols_task != "":
            df = separating_col_func(df, sep_cols_task)
        equiv_cols_task = intersection_cols(df, args.equivalent_columns)
        if equiv_cols_task != "" and equiv_cols_task != ":":
            df = equivalent_col_func(df, equiv_cols_task)
        df = flattening(df, equiv_cols_task, args.not_flatten_columns)
    return df


def argument_parser():

    # read arguments here
    parser = argparse.ArgumentParser(description="""Creator""")
    parser.add_argument(
        "--specific_query",
        action="store",
        dest="specific_query",
        default="",
        help="""Enter graphQL query.""",
    )
    parser.add_argument(
        "--compute_local",
        action="store",
        dest="compute_local",
        default="",
        help="""compute_local""",
    )
    parser.add_argument(
        "--apikey",
        action="store",
        dest="apikey",
        default="",
        help="""your personal api key from monday""",
    )

    parser.add_argument(
        "--equivalent_columns",
        action="store",
        dest="equivalent_columns",
        required=False,
        default="None",
        help="""multi-dimensional columns which are equivlanet with respect to their individual elements""",
    )
    parser.add_argument(
        "--separation_columns",
        action="store",
        dest="separation_columns",
        required=False,
        default="None",
        help="""multi-dimensional columns which""",
    )
    parser.add_argument(
        "--not_flatten_columns",
        action="store",
        dest="not_flatten_columns",
        required=False,
        default="None",
        help="""columns you wish to keep as list""",
    )
    return parser.parse_args()


def main():
    args = argument_parser()
    sq = args.specific_query
    apik = args.apikey
    # load apikey from environ variable
    try:
        key = os.environ["APIKEY"]
    except KeyError:
        key = apik

    apiUrl = "https://api.monday.com/v2"
    headers = {"Authorization": key}

    if sq != "":
        specificquery(sq, apiUrl, headers)
    else:
        boards_ids = save_workspace_boards(apiUrl, headers)
        boards(boards_ids, args, apiUrl, headers)


if __name__ == "__main__":
    main()
