import os
import csv
import getopt
import sys
import datetime
import os.path
import json
import requests
import pandas as pd
from urllib import parse
import argparse

def flatten_nested_json_df(df):

    df = df.reset_index()
    # search for columns to explode/flatten
    s = (df.applymap(type) == list).all()
    list_columns = s[s].index.tolist()

    s = (df.applymap(type) == dict).all()
    dict_columns = s[s].index.tolist()
    while len(list_columns) > 0 or len(dict_columns) > 0:
        new_columns = []

        for col in dict_columns:
            # explode dictionaries horizontally, adding new columns
            horiz_exploded = pd.json_normalize(df[col]).add_prefix(f'{col}.')
            horiz_exploded.index = df.index
            df = pd.concat([df, horiz_exploded], axis=1).drop(columns=[col])
            new_columns.extend(horiz_exploded.columns) # inplace

        for col in list_columns:
            # explode lists vertically, adding new columns
            df = df.drop(columns=[col]).join(df[col].explode().to_frame())
            new_columns.append(col)

        # check if there are still dict o list fields to flatten
        s = (df[new_columns].applymap(type) == list).all()
        list_columns = s[s].index.tolist()

        s = (df[new_columns].applymap(type) == dict).all()
        dict_columns = s[s].index.tolist()
    return df        

def get_all_data(api_key,count,object_list):
    for i in object_list:
        
        print(i)
        url = 'https://api.hubapi.com/crm/v3/objects/{}?count='.format(i)+str(count)+'&archived=false&hapikey='+access_token
        headers = {}
    
        r = requests.get(url = url, headers = headers)
        response_dict = json.loads(r.text)
        vars()[i] = pd.DataFrame(response_dict['results']) 
        vars()[i] = flatten_nested_json_df(vars()[i])
        vars()[i].drop('index',axis=1 , inplace=True)
        data = data.append(d[i])
        vars()[i].to_csv('/cnvrg/'+i+'.csv')
    return vars()[i]

if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(description="""Preprocessor""")
        
        parser.add_argument('--object_list', action='store', dest='object_list',
                            default = '', required=True, help="""list of objects to be fetched""")
        parser.add_argument('--access_token', action='store', dest='access_token',
                            default = '', required=True, help="""access_token""")
        
        parser.add_argument('--association_id_list', action='store', dest='association_id_list',
                            default = '', required=True, help="""list of id's to be assiciated""")
        parser.add_argument('--object_type', action='store', dest='object_type',
                            default = '', required=True, help="""object_type""")
        parser.add_argument('--to_object_type', action='store', dest='to_object_type',
                            default = '', required=True, help="""to_object_type""")
        
        parser.add_argument('--count', action='store', dest='count',
                            default = '', required=True, help="""count""")
        parser.add_argument('--project_dir', action='store', dest='project_dir',
                                help="""--- For inner use of cnvrg.io ---""")
        parser.add_argument('--output_dir', action='store', dest='output_dir',
                                help="""--- For inner use of cnvrg.io ---""")
        
        args = parser.parse_args()
        access_token = args.access_token
        count = int(args.count)
        object_list = args.object_list.split(',')
        object_list = list(map(str.lower,object_list))
        association_id_list = args.association_id_list.split(',')
        object_type = args.object_type
        to_object_type = args.to_object_type
        #load apikey from environ variable
        try:
            key = os.environ['ACCESS_TOKEN']
        except:
            key = access_token
            
        timestamp = datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d : %H:%M')
        print("DATE : ",timestamp,"\n")
        print("HubSpot data extraction process Started")
        
        #define authorizations
        headers = {
                'authorization': 'Bearer '+key,
            }
        
        #loop on the list of id's given to be assiciated b/w 2 objects
        for i in association_id_list:
            response = requests.get('https://api.hubapi.com/crm/v3/objects/first_object/{}/associations/{}'.format(object_type,i,to_object_type), headers = headers)
            try:
                response_dict = json.loads(response.text)
                vars()[i] = pd.DataFrame(response_dict['results']) 
                vars()[i].to_csv('/cnvrg/'+object_type+'_'+to_object_type+'.csv')
            except:
                pass
            
        # loop on all objects and fetch their data by calling api
        # not in scope means the user hasn't selected the called object as an object in the crm list
        # no data means the object has no data
        for i in object_list:
            print(i)
            
            response = requests.get('https://api.hubapi.com/crm/v3/objects/{}'.format(i), headers=headers)
            
            response_dict = json.loads(response.text)

            
            #feedback submissions is not in the scope of the account
            try:
                vars()[i] = pd.DataFrame(response_dict['results']) 
                try:
                    vars()[i] = flatten_nested_json_df(vars()[i])
                    vars()[i].drop('index',axis=1 , inplace=True)
                    vars()[i].to_csv('/cnvrg/'+i+'.csv')
                except KeyError as e:
                    print(e)
                    print(i+' has no data')
                    pass
            except KeyError as e:
                print(e)
                print(i+' is not in the scope of the account')

    except:
        print("HS_MAIN : data extraction processing Failed !!!!:", sys.exc_info())