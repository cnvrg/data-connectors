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

import argparse
import os
import snowflake.connector
import pandas as pd
import os
import sys

# setup a connection
def connect(password, warehouse, account, user, database, schema):

    try:
        conn = snowflake.connector.connect(
            user=user,
            password=password,
            account=account,
            warehouse=warehouse,
            database=database,
            schema=schema
        )
        return conn
    except Exception as e:
        print("Could not connect to snowflake, check your parameters")
        print(e)
        sys.exit(1)

# close the connection
def close_connection(conn=None):
    try:
        conn.cursor().close()
    except Exception as e:
        print("Could not close connection to snowflake")
        print(e)
        sys.exit(1)

# run the query
def run(conn=None, query=None):
    if query is None:
        print("Query can't be empty")
        sys.exit(1)
    try:
        return conn.cursor().execute(query)
    except Exception as e:
        print("Could not run query: %s" % query)
        print(e)
        sys.exit(1)

# output as a dataframe
def to_df(conn=None, query=None):
    cur = run(conn=conn, query=query)
    df = pd.DataFrame.from_records(
        iter(cur), columns=[
            x[0] for x in cur.description])
    return df

# output as a csv
def to_csv(conn=None, query=None, filename=None):
    cur = run(conn=conn, query=query)
    col_headers = [i[0] for i in cur.description]
    rows = [list(i) for i in cur.fetchall()]
    df = pd.DataFrame(rows, columns=col_headers)
    df.to_csv('/cnvrg/' + filename, index=False)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='set input arguments')
    parser.add_argument(
        '--user',
        action="store",
        dest='user',
        required=True,
        type=str,
        default='')
    parser.add_argument(
        '--account',
        action="store",
        dest='account',
        required=True,
        type=str,
        default='')
    parser.add_argument(
        '--warehouse',
        action="store",
        dest='warehouse',
        required=False,
        type=str,
        default='')
    parser.add_argument(
        '--database',
        action="store",
        dest='database',
        required=True,
        type=str,
        default='')
    parser.add_argument(
        '--schema',
        action="store",
        dest='schema',
        required=False,
        type=str,
        default='')
    parser.add_argument(
        '--password',
        action="store",
        dest='password',
        required=True,
        type=str,
        default='')
    parser.add_argument(
        '--query',
        action="store",
        dest='query',
        required=False,
        type=str,
        default='')
    parser.add_argument(
        '--filename',
        action="store",
        dest='filename',
        required=True,
        type=str,
        default='')
    parser.add_argument(
        '--dataset',
        action="store",
        dest='dataset',
        required=False,
        type=str,
        default='')
    args = parser.parse_args()

    # get confidentail parameters from args or os
    password = os.getenv('SNOWFLAKE_PASSWORD') or args.password
    warehouse = os.getenv('SNOWFLAKE_WAREHOUSE') or args.warehouse
    account = os.getenv('SNOWFLAKE_ACCOUNT') or args.account
    user = os.getenv('SNOWFLAKE_USER') or args.user
    query = args.query
    schema = args.schema
    filename = args.filename
    database = args.database
    dataset = args.dataset

    snf = connect(password, warehouse, account, user, database, schema)

    to_csv(conn=snf, query=query, filename=filename)
