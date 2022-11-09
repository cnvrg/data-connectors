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

# pip install simple_salesforce

# import required libraries
from simple_salesforce import Salesforce
from simple_salesforce.exceptions import SalesforceMalformedRequest
import pandas as pd
import requests
import json
import argparse
import os
import time
from datetime import datetime, timedelta
from collections import OrderedDict
import json

# define parser arguments
parser = argparse.ArgumentParser(description="""Preprocessor""")
parser.add_argument(
    '--column_list',
    action='store',
    dest='column_list',
    default='',
    required=True,
    help="""column_list""")
parser.add_argument(
    '--entity_definition_column_list',
    action='store',
    dest='entity_definition_column_list',
    default='',
    required=True,
    help="""entity_definition_column_list""")
parser.add_argument(
    '--limit',
    action='store',
    dest='limit',
    default='',
    required=False,
    help="""limit""")
parser.add_argument(
    '--start_date',
    action='store',
    dest='start_date',
    default='',
    required=True,
    help="""start_date""")
parser.add_argument(
    '--end_date',
    action='store',
    dest='end_date',
    default='',
    required=True,
    help="""end_date""")
parser.add_argument(
    '--extract_all_data',
    action='store',
    dest='extract_all_data',
    default='',
    required=True,
    help="""extract_all_data""")

parser.add_argument(
    '--username',
    action='store',
    dest='username',
    default='',
    required=True,
    help="""username""")
parser.add_argument(
    '--password',
    action='store',
    dest='password',
    default='',
    required=True,
    help="""password""")
parser.add_argument(
    '--security_token',
    action='store',
    dest='security_token',
    default='',
    required=True,
    help="""security_token""")

parser.add_argument(
    '--compute',
    action='store',
    dest='compute',
    default='small',
    required=False,
    help="""compute""")
parser.add_argument('--project_dir', action='store', dest='project_dir',
                    help="""--- For inner use of cnvrg.io ---""")
parser.add_argument('--output_dir', action='store', dest='output_dir',
                    help="""--- For inner use of cnvrg.io ---""")


# call parser arguments
args = parser.parse_args()
column_list = args.column_list.split(",")
entity_definition_column_list = args.entity_definition_column_list.split(",")
limit = int(args.limit)
start_date = args.start_date
end_date = args.end_date
extract_all_data = args.extract_all_data
username = args.username
password = args.password
try:
    username = os.environ['SALESFORCE_USERNAME']
except BaseException:
    username = args.username
try:
    password = os.environ['SALESFORCE_PASSWORD']
except BaseException:
    password = args.password
try:
    security_token = os.environ['SALESFORCE_SECURITY_TOKEN']
except BaseException:
    security_token = args.security_token


def data_extraction(field_name, limit):
    """
    Parameters
    ----------
    field_name : string for column name
    limit : limit the number of rows to be pulled

    Returns
    -------
    df : dataframe pulled with the help of query for that column
    """
    # sql query to pull data
    if limit <= 0:
        soql = "SELECT Name, EntityDefinition.QualifiedApiName FROM EntityParticle WHERE EntityDefinition.QualifiedApiName ='{}'".format(
            field_name)
    else:
        soql = "SELECT Name, EntityDefinition.QualifiedApiName FROM EntityParticle WHERE EntityDefinition.QualifiedApiName ='{}' limit {}".format(
            field_name, limit)
    results1 = bulk.query_all(soql)
    df = pd.DataFrame(index=range(len(results1['records'])), columns=[
                      'Name', 'EntityDefinition'])
    for i in df.index:
        df.loc[i, 'Name'] = results1['records'][i]['EntityDefinition']['QualifiedApiName']
        df.loc[i, 'EntityDefinition'] = results1['records'][i]['Name']
    return df


def safeIntegerInput(num_retries=3):
    '''
    Parameters
    ----------
    num_retries : number of retries before it terminates the connection
        DESCRIPTION. The default is 3.
    Raises
    ------
    error
    '''
    for attempt_no in range(num_retries):
        try:
            return int(input("Importance:\n\t1: High\n\t2: Normal\n\t3: Low"))
        except ValueError as error:
            if attempt_no < (num_retries - 1):
                print("Error: Invalid number")
            else:
                raise error

# create timeout adaptor for requests


class TimeoutAdapter(requests.adapters.HTTPAdapter):
    def send(self, *args, **kwargs):
        kwargs['timeout'] = 30
        return super().send(*args, **kwargs)


if __name__ == '__main__':
    try:
        # call the defined parser arguments
        field_name_lst = column_list
        print(field_name_lst)
        final_dataframe = pd.DataFrame()
        print(entity_definition_column_list)
        limit = limit
        if len(end_date) <= 0 and len(start_date) <= 0:
            end_date = datetime.today().strftime('%Y-%m-%d')
            last_week_date = datetime.today() - timedelta(days=7)
            start_date = last_week_date.strftime('%Y-%m-%d')
            start_date = start_date + 'T00:00:00Z'
            end_date = end_date + 'T23:59:59Z'
        elif len(end_date) <= 0 and len(start_date) > 0:
            end_date = datetime.today().strftime('%Y-%m-%d')
            start_date = start_date + 'T00:00:00Z'
            end_date = end_date + 'T23:59:59Z'
        elif len(start_date) <= 0 and len(end_date) > 0:
            last_week_date = datetime.today() - timedelta(days=7)
            start_date = last_week_date.strftime('%Y-%m-%d')
            start_date = start_date + 'T00:00:00Z'
            end_date = end_date + 'T23:59:59Z'
        else:
            start_date = start_date + 'T00:00:00Z'
            end_date = end_date + 'T23:59:59Z'
        sfSession = requests.Session()
        sfSession.mount("https://", TimeoutAdapter())

        # initiate bulk queries
        bulk = Salesforce(
            username=username,
            password=password,
            security_token=security_token,
            domain='test',
            session=sfSession)
        bulk1 = Salesforce(
            username=username,
            password=password,
            security_token=security_token,
            domain='test',
            session=sfSession)

        for i in range(len(field_name_lst)):
            print(field_name_lst[i])
            final_dataframe = final_dataframe.append(
                data_extraction(field_name_lst[i], limit))
        final_dataframe.to_csv(
            "/cnvrg/Name_EntityDefinition_Dataframe.csv",
            index=False)

        # to extract all the columns in the tables
        if extract_all_data == 'yes':
            entity_definition_column_list = final_dataframe['EntityDefinition'].tolist(
            )

        fields_to_get = final_dataframe
        fields_to_get = fields_to_get.reset_index().drop('index', axis=1)
        fields_to_get_1 = fields_to_get
        if len(entity_definition_column_list) > 0:
            fields_to_get_1 = fields_to_get_1[fields_to_get_1["EntityDefinition"].isin(
                entity_definition_column_list)]
        fields_to_get_1 = fields_to_get_1[fields_to_get_1["Name"].isin(
            field_name_lst)]
        fields_to_get_1['Concatenated'] = fields_to_get_1['Name'] + \
            ' - ' + fields_to_get_1['EntityDefinition']
        fields_to_get_1['CreatedDate'] = 'CreatedDate'
        fields_to_get_1 = fields_to_get_1.reset_index().drop('index', axis=1)
        list_1 = fields_to_get_1['Concatenated'].to_list()
        output_df = pd.DataFrame(columns=list_1)

        retries = 4
        for i in range(len(fields_to_get_1)):
            if limit <= 0:
                query_i = 'Select CreatedDate,' + fields_to_get_1['EntityDefinition'][i] + ' from ' + \
                    fields_to_get_1['Name'][i] + ' where CreatedDate>={} and CreatedDate<={}'.format(start_date, end_date)
            else:
                query_i = 'Select CreatedDate,' + fields_to_get_1['EntityDefinition'][i] + ' from ' + fields_to_get_1['Name'][i] + \
                    ' where CreatedDate>={} and CreatedDate<={}'.format(start_date, end_date) + ' limit {}'.format(limit)
                print(query_i)
            for attempt_no in range(retries):
                try:
                    output = bulk.query(query_i)

                except ConnectionError as error:
                    if(attempt_no < (retries - 1)):
                        print("Trying again")
                    else:
                        raise error
                        print("Increase Timeout")
                except SalesforceMalformedRequest:
                    pass
            for j in range(len(output['records'])):
                if(output['records'][j][fields_to_get_1['EntityDefinition'][i]] == ''):
                    output_df.at[j,
                                 str(fields_to_get_1['Concatenated'][i])] = ' '
                    output_df.at[j,
                                 str(fields_to_get_1['CreatedDate'][i])] = ' '
                else:
                    output_df.at[j, str(fields_to_get_1['Concatenated'][i])
                                 ] = output['records'][j][fields_to_get_1['EntityDefinition'][i]]
                    output_df.at[j, str(fields_to_get_1['CreatedDate'][i])
                                 ] = output['records'][j][fields_to_get_1['CreatedDate'][i]]

        # get columns with addresses in a list
        address_col = [col for col in output_df.columns if 'Address' in col]

        # split the main dataframe into multiple dataframes based on their
        # object name
        for j in address_col:
            for idx, i in enumerate(output_df[j]):
                # convert to dict
                try:
                    output_df.loc[idx, j] = list(i.items())
                except AttributeError:
                    pass
        for j in address_col:
            for k in range(len(output_df)):
                for i in range(10):
                    try:
                        output_df.loc[k, '{} - '.format(j) +
                                      output_df[j][k][i][0]] = output_df[j][k][i][1]
                    except TypeError:
                        pass

        output_df = output_df.drop(address_col, axis=1)

        for i in field_name_lst:
            vars()[i] = output_df.filter(regex=str(i) + ' - ')
            vars()[i].to_csv("/cnvrg/{}.csv".format(i), index=False)

        output_df.to_csv("/cnvrg/output.csv", index=False)
        print('Code ran successfully')
    except RuntimeError as e:
        print(e)
