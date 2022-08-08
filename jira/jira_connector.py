from jira import JIRA
import json
import pandas as pd
import argparse
import sys
import os

if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(description="""Preprocessor""")
        parser.add_argument('--jql_query_for_issues', action='store', dest='jql_query_for_issues',
                            default = '', required=True, help="""jql query""")
        parser.add_argument('--project_list', action='store', dest='project_list',
                            default = '', required=True, help="""list of projects""")
        parser.add_argument('--project_object_list', action='store', dest='project_object_list',
                            default = '', required=True, help="""list of objects to be fetched""")
        parser.add_argument('--username', action='store', dest='username',
                            default = '', required=True, help="""username""")
        parser.add_argument('--api_key', action='store', dest='api_key',
                            default = '', required=True, help="""api_key""")
        parser.add_argument('--issue_object_list', action='store', dest='issue_object_list',
                            default = '', required=True, help="""list of objects in issues to be fetched""")
        parser.add_argument('--jira_url', action='store', dest='jira_url',
                            default = '', required=True, help="""url for jira server""")
        parser.add_argument('--project_dir', action='store', dest='project_dir',
                                help="""--- For inner use of cnvrg.io ---""")
        parser.add_argument('--output_dir', action='store', dest='output_dir',
                                help="""--- For inner use of cnvrg.io ---""")

        args = parser.parse_args()

        jql_query_for_issues = args.jql_query_for_issues
        project_list = args.project_list.split(',')
        project_object_list = args.project_object_list.split(',')
        print('List of Projects:')
        print(project_object_list)
        
        username = args.username
        try:
            username = os.environ['USER_NAME']
        except:
            username = username
        print('Username = '+username)
        
        api_key = args.api_key
        try:
            api_key = os.environ['API_KEY']
        except:
            api_key = api_key
        print('API Key = '+api_key)
        
        issue_object_list = args.issue_object_list.split(',')
        print('List of Single Issues:')
        print(issue_object_list)
        jira_url = args.jira_url
        ################# Project specific #################]

        # hit jira server url
        jiraOptions = {'server': "{}".format(jira_url)}
        jira = JIRA(options=jiraOptions, basic_auth=(username, api_key))

        # define projects
        projects = jira.projects()

        prj = []
        if len(project_list)<=1: # see if the length of the project_list argument is <=1 meaning no data is given in the arg
            for i in range(len(projects)):
                a = projects[i].key
                prj.append(a)
            project_list = prj # make a default project list including all the projects


        project_data = pd.DataFrame()
        for i in project_list: # loop on list of projects and fetch required data 
            print(i)
            jra = jira.project(i)
            df  = pd.json_normalize(jra.raw)

            project_data = project_data.append(df)

        project_data = project_data.reset_index(drop=True)
        project_data = project_data[project_object_list] #filter the required project objects from the data
        project_data.to_csv('/cnvrg/project_data.csv')

        ############### Issue Specific ########################

        issue_data = pd.DataFrame()
        for singleIssue in jira.search_issues(jql_str = jql_query_for_issues, maxResults=1000): #loop on all issues in a project
            print(singleIssue)

            df  = pd.json_normalize(singleIssue.raw)
            issue_data = issue_data.append(df)
        issue_data = issue_data.reset_index(drop=True)
        issue_data = issue_data[issue_object_list] #filter required data from issues
        issue_data.to_csv('/cnvrg/issue_data.csv')
    
    except:
        print("JIRA_MAIN : data extraction processing Failed !!!!:", sys.exc_info())