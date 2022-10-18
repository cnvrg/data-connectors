import requests
import json
import argparse
import time
import pandas as pd
import os
from flattening import separating_col_func, explode_multiple, equivalent_col_func, flattening, intersection_cols
cnvrg_workdir = os.environ.get("CNVRG_WORKDIR", "/cnvrg")


"""
This function takes input a GraphQL query and saves the reponse as a json file.
"""
def specificquery(sq):
    data = {'query': sq}
    r = requests.post(url=apiUrl, json=data, headers=headers)  # make request
    returns = r.json()
    print(returns)
    try:
        returns = returns["data"]
    except:
        if "Complexity budget exhausted" in returns["errors"][0]['message']:
            print("going to wait 60sec because complexity budget exhausted")
            time.sleep(60)
            r = requests.post(url=apiUrl, json=data, headers=headers)
            returns = r.json()
            returns = returns["data"]
        else:
            raise Exception(returns)
    # save the json response
    json_object = json.dumps(returns, indent=4)
    with open(cnvrg_workdir+"/specific.json", "w") as outfile:
        outfile.write(json_object)


"""
This function creates two CSVs one for all workspaces and one for all boards contanining high level information
"""


def boards_and_workspaces():
    query = "{ boards { name id workspace {id name description kind} permissions owners{name}}}"
    data = {"query": query}
    print("querying all boards")
    r = requests.post(url=apiUrl, json=data, headers=headers)  # make request
    boards = r.json()
    board_ids = []
    if "errors" in boards.keys():
        raise Exception(boards["errors"])
    else:
        workspaces_id = {}
        df_workspace = pd.DataFrame(columns=["id", "name", "kind", "description"])
        df_boards = pd.DataFrame(
            columns=["board_id", "workspace_id", "name", "owners", "permissions"]
        )
        for i, board in enumerate(boards["data"]["boards"]):
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
            except TypeError:  # if the workspace is None
                pass
        print("saving boards and workspaces")
        df_boards.to_csv(cnvrg_workdir+"/boards.csv")
        df_workspace.to_csv(cnvrg_workdir+"/workspaces.csv")
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
This function creates one csv per board containing all the necessary in the board
"""


def boards(boardids):
    for everyboard in boardids:
        print("querying board id: "+everyboard)
        query = (
            "{ boards (ids:"
            + everyboard
            + ") {     items { id name subscribers {name} column_values { title text } subitems { name  }}}}"
        )
        data = {"query": query}
        r = requests.post(url=apiUrl, json=data, headers=headers)
        returns = r.json()
        try:
            returns = returns["data"]
        except:

            if "Complexity budget exhausted" in returns["error_message"]:
                print("going to wait 60sec because complexity budget exhausted")
                time.sleep(60)
                r = requests.post(url=apiUrl, json=data, headers=headers)
                returns = r.json()
                returns = returns["data"]
                
            else:
                raise (returns)
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
        
            #run flattening on df
        sep_cols_task = intersection_cols(df, sep_cols)
        if sep_cols_task != '':
            df = separating_col_func(df, sep_cols_task)
        equiv_cols_task = intersection_cols(df, equiv_cols)
        if equiv_cols_task != '' and equiv_cols_task != ':':
            df = equivalent_col_func(df, equiv_cols_task)
        df = flattening(df, equiv_cols_task, not_flat)
                
        print("saving board id: "+everyboard)
        df.to_csv(cnvrg_workdir+"/"+everyboard + ".csv")


if __name__ == "__main__":

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
        "--apikey", action="store", dest="apikey", default="", help="""your personal api key from monday""",
    )
    
    parser.add_argument(
        "--equivalent_columns",
        action="store",
        dest="equivalent_columns",
        required=False,
        default = "None",
        help="""multi-dimensional columns which are equivlanet with respect to their individual elements""",
    )
    parser.add_argument(
        "--separation_columns",
        action="store",
        dest="separation_columns",
        required=False,
        default = "None",
        help="""multi-dimensional columns which""",
    )
    parser.add_argument(
        "--not_flatten_columns",
        action="store",
        dest="not_flatten_columns",
        required=False,
        default = "None",
        help="""columns you wish to keep as list""",
    )
    args = parser.parse_args()
    sq = args.specific_query
    apik = args.apikey
    equiv_cols = args.equivalent_columns
    sep_cols = args.separation_columns
    not_flat = args.not_flatten_columns
    do_flattening = True
    if(equiv_cols is None or sep_cols is None):
        do_flattening = False
        
    # load apikey from environ variable
    try:
        key = os.environ["APIKEY"]
    except:
        key = apik

    apiUrl = "https://api.monday.com/v2"
    headers = {"Authorization": key}

    if sq != "":
        specificquery(sq)
    else:
        boards_ids = boards_and_workspaces()
        boards(boards_ids)