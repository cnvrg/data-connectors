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

import json
import asana
import pandas as pd
import os
import argparse
import requests
from io import StringIO
import os

parser = argparse.ArgumentParser(description="""Creator""")
parser.add_argument(
    "-f",
    "--access_token",
    action="store",
    dest="access_token",
    default="sdfsdmflskdfsdklf",
    required=True,
    help="""access token value (PAT) """,
)
parser.add_argument(
    "--workspace",
    action="store",
    dest="workspace",
    default="workspace2",
    required=True,
    help="""name of the workspace you want to filter on """,
)
parser.add_argument(
    "--project",
    action="store",
    dest="project",
    default="Scorpicore",
    required=True,
    help="""name of the project you want to filter on""",
)
parser.add_argument(
    "--query",
    action="store",
    dest="query",
    default="https://app.asana.com/api/1.0/tasks/1202266946298519",
    required=True,
    help="""curl query you want to execute """,
)
parser.add_argument(
    "--task_due_date",
    action="store",
    dest="task_due_date",
    default="2022-05-28,2022-04-22",
    required=True,
    help="""start and end dates for task due date """,
)
parser.add_argument(
    "--task_start_date",
    action="store",
    dest="task_start_date",
    default="2022-05-28,2022-04-22",
    required=True,
    help="""start and end dates for task start date""",
)
parser.add_argument(
    "--premium_account",
    action="store",
    dest="premium_account",
    default="Yes",
    required=True,
    help="""whether the asana account is premium or not""",
)
parser.add_argument(
    "--equivalent_columns",
    action="store",
    dest="equivalent_columns",
    default="Task-Comment Gid,Task-Comment Created At,Task-Comment Text,Task-Comment Created By,Task-Comment Resource SubType,:,Sub-Task Comment Gid,Sub-Task Comment Created At,Sub-Task Comment Text,Sub-Task Comment Created By,Sub-Task Comment Resource Subtype",
    required=True,
    help="""multi-dimensional columns which are equivlanet with respect to their individual elements""",
)
parser.add_argument(
    "--separation_columns",
    action="store",
    dest="separation_columns",
    default="Sub-Task Attachment,Team Name",
    required=True,
    help="""multi-dimensional columns which""",
)
parser.add_argument(
    "--not_flatten_columns",
    action="store",
    dest="not_flatten_columns",
    default="Tag-ID, Tag Name",
    required=True,
    help="""columns you wish to keep as list""",
)


args = parser.parse_args()
access_token = args.access_token
workspace_param = args.workspace.split(',')
project_param = args.project.split(',')
query = args.query
task_due_date = args.task_due_date.split(',')
task_start_date = args.task_start_date.split(',')
prem_act = args.premium_account
equiv_cols = args.equivalent_columns
sep_cols = args.separation_columns
not_flat = args.not_flatten_columns

if os.environ.get('access_token') == 'True':
    PAT = os.environ['access_token']
else:
    PAT = access_token

client = asana.Client.access_token(PAT)
me = client.users.me()


if query == 'None':
    #PAT = '1/1202266991680810:8378229ef7d219bc520cae6c8a69ed73'
    workspace_list = [x['gid'] for x in me['workspaces']]
    workspace_list_0 = [x['gid']+'-'+x['name'] for x in me['workspaces']]
    projects = [client.projects.find_by_workspace(x,{"opt_fields":["gid","name","resource_type","workspace","status_updates"]} ,iterator_type=None) for x in workspace_list]

    task_frame = pd.DataFrame(columns = ['Sub-Task ID', 'Sub-Task Name'
    ,'Sub-Task Assignee ID','Sub-Task Assignee Name','Sub-Task Comment Gid','Sub-Task Comment Created At','Sub-Task Comment Text','Sub-Task Comment Created By','Sub-Task Comment Resource Subtype','Sub-Task Completed By','Sub-Task Completed At', 'Sub-Task Custom Field Name','Sub-Task Custom Field Value','Sub-Task Dependencies','Sub-Task Start On','Sub-Task Due On','Sub-Task Notes','Sub-Task Tags','Sub-Task Attachment','Task-ID','Task-Name','Task-Assignee ID','Task-Assignee Name','Task-Completed By','Task-Completed At','Task-Custom Field Name','Task-Custom Field Value','Task-Dependencies','Task-Start On','Task-Due On','Task-Tags','Task-Notes','Task-Comment Gid','Task-Comment Created At','Task-Comment Text','Task-Comment Created By','Task-Comment Resource SubType','Task-Attachment','Project Name','Project ID'])

    for project in projects:
        for proj in project:
            project_id = proj['gid']
            project_tasks = client.tasks.find_by_project(project_id, {"opt_fields":["this.notes","name","description","Dependencies","due_on","resource_type","start_on","assignee","Completed_By","Description","notes","tags","this.name","custom_fields","priorty","completed_at","attachment"]},  iterator_type=None)
            for task in project_tasks:

                task_id = task['gid']
                task_subtasks = client.tasks.subtasks(task_id, {"opt_fields":["this.notes","name","description","Dependencies","due_on","resource_type","start_on","assignee","Completed_By","Description","notes","tags","this.name","custom_fields","priorty","completed_at"]}, full_payload=True, opt_pretty = True)
                task_comments = client.tasks.stories(task_id, full_payload=True)
                task_attach = client.attachments.find_by_task(task_id, {"opt_fields":["download_url","view_url","permanent_url","gid","name","resource_subtype"]})
                sub_task_frame = pd.DataFrame(columns = ['Sub-Task ID', 'Sub-Task Name', 'Sub-Task Assignee ID','Sub-Task Assignee Name','Sub-Task Comment Gid','Sub-Task Comment Created At','Sub-Task Comment Text','Sub-Task Comment Created By','Sub-Task Comment Resource Subtype','Sub-Task Completed By','Sub-Task Completed At', 'Sub-Task Custom Field Name','Sub-Task Custom Field Value','Sub-Task Dependencies','Sub-Task Start On','Sub-Task Due On','Sub-Task Notes','Sub-Task Tags','Sub-Task Attachment'])
                sub_cnt = 0
                for subtask in task_subtasks:
                    print(sub_cnt)
                    sub0 = []
                    sub1 = []
                    sub2 = []
                    sub3 = []
                    sub4 = []
                    sub5 = []
                    att0 = []
                    att2 = []
                    subtask_id = subtask['gid']
                    subtask_comments = client.tasks.stories(subtask_id, full_payload=True)
                    attach = client.attachments.find_by_task(subtask_id, {"opt_fields":["download_url","view_url","permanent_url","gid","name","resource_subtype"]})
                    if prem_act.lower() == 'yes':
                        len_custom_fields = len(subtask['custom_fields'])
                    else:
                        len_custom_fields = 0
                    sub_task_frame.at[sub_cnt,'Sub-Task Name'] = subtask['name']
                    sub_task_frame.at[sub_cnt,'Sub-Task ID'] = subtask['gid']
                    if subtask['assignee'] == None:
                        sub_task_frame.at[sub_cnt,'Sub-Task Assignee ID'] = ''
                        sub_task_frame.at[sub_cnt,'Sub-Task Assignee Name'] = ''
                    else:
                        sub_task_frame.at[sub_cnt,'Sub-Task Assignee ID'] = client.users.get_user(subtask['assignee']['gid'])['gid']
                        sub_task_frame.at[sub_cnt,'Sub-Task Assignee Name'] = client.users.get_user(subtask['assignee']['gid'])['name']

                    if subtask['completed_by'] == None:
                        sub_task_frame.at[sub_cnt,'Sub-Task Completed By'] = ''
                    else:
                        sub_task_frame.at[sub_cnt,'Sub-Task Completed By'] = client.users.get_user(subtask['completed_by']['gid'])['name']

                    sub_task_frame.at[sub_cnt,'Sub-Task Completed At'] = subtask['completed_at']
                    if len_custom_fields == 0:
                        sub_task_frame.at[sub_cnt,'Sub-Task Custom Field Name'] = ''
                        sub_task_frame.at[sub_cnt,'Sub-Task Custom Field Value'] = ''
                    elif len_custom_fields > 1:
                        sub_task_frame.at[sub_cnt,'Sub-Task Custom Field Name'] = [x['gid'] for x in subtask['custom_fields']]
                        sub_task_frame.at[sub_cnt,'Sub-Task Custom Field Value'] = [x['name'] for x in subtask['custom_fields']]
                    else:
                        sub_task_frame.at[sub_cnt,'Sub-Task Custom Field Name'] = subtask['custom_fields'][0]['name']
                        sub_task_frame.at[sub_cnt,'Sub-Task Custom Field Value'] = subtask['custom_fields'][0]['gid']                    
                    if prem_act.lower() == 'yes':
                        sub_task_frame.at[sub_cnt,'Sub-Task Dependencies'] = subtask['dependencies']
                    else:
                        sub_task_frame.at[sub_cnt,'Sub-Task Dependencies'] = ''

                    sub_task_frame.at[sub_cnt,'Sub-Task Start On'] = subtask['start_on']
                    sub_task_frame.at[sub_cnt,'Sub-Task Due On'] = subtask['due_on']
                    sub_task_frame.at[sub_cnt,'Sub-Task Tags'] = [x['gid'] for x in subtask['tags']]
                    sub_task_frame.at[sub_cnt,'Sub-Task Notes'] = subtask['notes']
                    for jk in attach:
                        temp_url = '=HYPERLINK("https://' + jk["permanent_url"] +'","' + jk['name']+'")' 
                        att2.append(temp_url)
                    for j in subtask_comments:
                        sub1.append(j['gid'])
                        sub2.append(j['created_at'])
                        sub3.append(j['text'])
                        sub4.append(j['created_by']['name'])
                        sub5.append(j['resource_subtype'])
                    sub0.append(sub1)
                    sub0.append(sub2)
                    sub0.append(sub3)
                    sub0.append(sub4)
                    sub0.append(sub5)
                    att0.append(att2)

                    if sub0 != [] or sub0 != '':
                        sub_task_frame.at[sub_cnt,'Sub-Task Comment Gid'] = [sub0[0] for i in sub_task_frame.index][0]
                        sub_task_frame.at[sub_cnt,'Sub-Task Comment Created At'] = [sub0[1] for i in sub_task_frame.index][0]
                        sub_task_frame.at[sub_cnt,'Sub-Task Comment Text'] = [sub0[2] for i in sub_task_frame.index][0]
                        sub_task_frame.at[sub_cnt,'Sub-Task Comment Created By'] = [sub0[3] for i in sub_task_frame.index][0]
                        sub_task_frame.at[sub_cnt,'Sub-Task Comment Resource Subtype'] = [sub0[4] for i in sub_task_frame.index][0]
                        sub_task_frame.at[sub_cnt,'Sub-Task Attachment'] = att0[0]
                    sub_cnt = sub_cnt+1
                if len(sub_task_frame) == 0:
                    cnt_add = 0
                    for (columnName, columnData) in sub_task_frame.iteritems():
                        sub_task_frame.at[cnt_add,columnName] = ''

                sub_task_frame['Task-ID'] = task['gid']
                sub_task_frame['Task-Name'] = task['name']
                if task['assignee'] == None:
                    sub_task_frame['Task-Assignee ID'] = ''
                    sub_task_frame['Task-Assignee Name'] = ''
                else:
                    sub_task_frame['Task-Assignee ID'] = client.users.get_user(task['assignee']['gid'])['gid']
                    sub_task_frame['Task-Assignee Name'] = client.users.get_user(task['assignee']['gid'])['name']
                if task['completed_by'] == None:
                    sub_task_frame['Task-Completed By'] = ''
                else:
                    sub_task_frame['Task-Completed By'] = client.users.get_user(task['completed_by']['gid'])['name']

                sub_task_frame['Task-Completed At'] = task['completed_at']
                if prem_act.lower() == 'yes':
                    len_custom_fields = len(task['custom_fields'])
                else:
                    len_custom_fields = 0
                if len_custom_fields == 0:
                    sub_task_frame['Task-Custom Field Name'] = ''
                    sub_task_frame['Task-Custom Field Value'] = ''
                elif len_custom_fields > 1:
                    custom_field_name = [x['name'] for x in task['custom_fields']]
                    custom_field_val = [x['display_value'] for x in task['custom_fields']]
                    sub_task_frame['Task-Custom Field Name'] = [custom_field_name for _ in range(len(sub_task_frame))]
                    sub_task_frame['Task-Custom Field Value'] = [custom_field_val for _ in range(len(sub_task_frame))]
                else:
                    print('end')
                    sub_task_frame['Task-Custom Field Name'] = task['custom_fields'][0]['name']
                    sub_task_frame['Task-Custom Field Value'] = task['custom_fields'][0]['display_value']
                if prem_act.lower() == 'yes':
                    sub_task_frame['Task-Dependencies'] = [task['dependencies'] for _ in range(len(sub_task_frame))]
                else:
                    sub_task_frame['Task-Dependencies'] = ''
                sub_task_frame['Task-Start On'] = task['start_on']
                sub_task_frame['Task-Due On'] = task['due_on']
                sub_task_frame['Task-Tags'] = [[x['gid'] for x in task['tags']] for _ in range(len(sub_task_frame))]

                sub_task_frame['Task-Notes'] = task['notes']
                tas0 = []
                tas1 = []
                tas2 = []
                tas3 = []
                tas4 = []
                tas5 = []
                tat0 = []
                tat2 = []
                for klo in task_attach:
                    temp1_url = '=HYPERLINK("https://' + klo["permanent_url"] +'","' + klo['name']+'")' 
                    tat2.append(temp1_url)
                for fj in task_comments:
                    tas1.append(fj['gid'])
                    tas2.append(fj['created_at'])
                    tas3.append(fj['text'])
                    tas4.append(fj['created_by']['name'])
                    tas5.append(fj['resource_subtype'])
                tas0.append(tas1)
                tas0.append(tas2)
                tas0.append(tas3)
                tas0.append(tas4)
                tas0.append(tas5)
                tat0.append(tat2)
                sub_task_frame['Task-Comment Gid'] = [tas0[0] for _ in range(len(sub_task_frame))]
                sub_task_frame['Task-Comment Created At'] = [tas0[1] for _ in range(len(sub_task_frame))]
                sub_task_frame['Task-Comment Text'] = [tas0[2] for _ in range(len(sub_task_frame))]
                sub_task_frame['Task-Comment Created By'] = [tas0[3] for _ in range(len(sub_task_frame))]
                sub_task_frame['Task-Comment Resource SubType'] = [tas0[4] for _ in range(len(sub_task_frame))]
                sub_task_frame['Task-Attachment'] = [tat0[0] for _ in range(len(sub_task_frame))]
                sub_task_frame['Project Name'] = proj['name']
                sub_task_frame['Project ID'] = proj['gid']
                sub_task_frame['Workspace ID'] = proj['workspace']['gid']

                task_frame = pd.concat([task_frame,sub_task_frame])

    task_frame1 = task_frame[['Workspace ID','Project ID','Project Name','Task-ID','Task-Name','Task-Assignee ID','Task-Assignee Name','Task-Completed By','Task-Completed At','Task-Custom Field Name','Task-Custom Field Value','Task-Dependencies','Task-Start On','Task-Due On','Task-Tags','Task-Notes','Task-Comment Gid','Task-Comment Created At','Task-Comment Text','Task-Comment Created By','Task-Comment Resource SubType','Task-Attachment','Sub-Task ID','Sub-Task Name','Sub-Task Assignee ID','Sub-Task Assignee Name','Sub-Task Comment Gid','Sub-Task Comment Created At','Sub-Task Comment Text','Sub-Task Comment Created By','Sub-Task Comment Resource Subtype','Sub-Task Completed By','Sub-Task Completed At', 'Sub-Task Custom Field Name','Sub-Task Custom Field Value','Sub-Task Dependencies','Sub-Task Start On','Sub-Task Due On','Sub-Task Notes','Sub-Task Tags','Sub-Task Attachment']]
    task_frame_updated = task_frame1.reset_index()
    workspace_frame = pd.DataFrame(columns=['Workspace ID','Workspace Name','Team Name'])

    workspace_frame_updated = pd.DataFrame(columns=['Workspace ID','Workspace Tag','Workspace Tag Name'])

    goals_frame = pd.DataFrame(columns = ['Workspace ID','Goal Name','Goal Owner','Goal Due On','Goal Start On','Goal Status','Goal Notes','Goal Metric Currency','Goal Metric Initial','Goal Metric Target', 'Goal Metric Current','Goal Metric Unit'])
    portfolio_frame = pd.DataFrame(columns = ['Workspace ID','Portfolio Created At','Portfolio Created By','Portfolio Custom Field Setting','Portfolio Name'])

    cnt_w = 0
    cnt_g = 0
    cnt_p = 0
    cnt_t = 0
        
    for x in workspace_list_0:
        team_name_string = ''

        team_info = client.teams.get_teams_for_organization(x.split('-')[0],{"opt_fields":["gid","name","resource_type"]})
        tag_names = client.tags.get_tags_for_workspace(x.split('-')[0], {'param': 'value', 'param': 'value'}, opt_pretty=True)

        if prem_act.lower() == 'yes':
            goals_w = client.goals.get_goals({'workspace' : x.split('-')[0]}, opt_pretty=True)
            portfolio_w = client.portfolios.get_portfolios({'workspace': x.split('-')[0], 'owner': me['gid']}, opt_pretty=True)
            for i in goals_w:
                goal_info = client.goals.get_goal(i['gid'], {'param': 'value', 'param': 'value'}, opt_pretty=True)
                goals_frame.at[cnt_g,'Workspace ID'] = x.split('-')[0]
                goals_frame.at[cnt_g,'Goal Name'] = goal_info['name']
                goals_frame.at[cnt_g,'Goal Owner'] = goal_info['owner']['name']
                goals_frame.at[cnt_g,'Goal Due On'] = goal_info['due_on']
                goals_frame.at[cnt_g,'Goal Start On'] = goal_info['start_on']
                goals_frame.at[cnt_g,'Goal Status'] = goal_info['status']
                goals_frame.at[cnt_g,'Goal Notes'] = goal_info['notes']
                goals_frame.at[cnt_g,'Goal Metric Unit'] = goal_info['metric']['unit']
                goals_frame.at[cnt_g,'Goal Metric Currency'] = goal_info['metric']['currency_code']
                goals_frame.at[cnt_g,'Goal Metric Initial'] = goal_info['metric']['initial_number_value']
                goals_frame.at[cnt_g,'Goal Metric Target'] = goal_info['metric']['target_number_value']
                goals_frame.at[cnt_g,'Goal Metric Current'] = goal_info['metric']['current_number_value']
                cnt_g = cnt_g + 1
                
            for i in portfolio_w:
                portfolio_info = client.portfolios.get_portfolio(i['gid'], {"opt_fields":["gid","name","resource_type","created_by","created_at","current_status_update","custom_field_settings"]},opt_pretty=True)
                portfolio_frame.at[cnt_p,'Workspace ID'] = x.split('-')[0]
                portfolio_frame.at[cnt_p,'Portfolio Created At'] = portfolio_info['created_at']
                portfolio_frame.at[cnt_p,'Portfolio Created By'] = client.users.get_user(portfolio_info['created_by']['gid'])['name']
                portfolio_frame.at[cnt_p,'Portfolio Name'] = portfolio_info['name']
                cnt_p = cnt_p + 1

        else:
            goals_frame.at[cnt_g,'Workspace ID'] = x.split('-')[0]
            goals_frame.at[cnt_g,'Goal Name'] = ''
            goals_frame.at[cnt_g,'Goal Owner'] = ''
            goals_frame.at[cnt_g,'Goal Due On'] = ''
            goals_frame.at[cnt_g,'Goal Start On'] = ''
            goals_frame.at[cnt_g,'Goal Status'] = ''
            goals_frame.at[cnt_g,'Goal Notes'] = ''
            goals_frame.at[cnt_g,'Goal Metric Unit'] = ''
            goals_frame.at[cnt_g,'Goal Metric Currency'] = ''
            goals_frame.at[cnt_g,'Goal Metric Initial'] = ''
            goals_frame.at[cnt_g,'Goal Metric Target'] = ''
            goals_frame.at[cnt_g,'Goal Metric Current'] = ''
            
            portfolio_frame.at[cnt_p,'Workspace ID'] = x.split('-')[0]
            portfolio_frame.at[cnt_p,'Portfolio Created At'] = ''
            portfolio_frame.at[cnt_p,'Portfolio Created By'] = ''
            portfolio_frame.at[cnt_p,'Portfolio Name'] = ''

        for i in team_info:
            team_name_string = team_name_string+','+i['name']

        workspace_frame.at[cnt_w,'Workspace ID'] = x.split('-')[0]
        workspace_frame.at[cnt_w,'Workspace Name'] = x.split('-')[1]
        workspace_frame.at[cnt_w,'Team Name'] = team_name_string[1:].split(',')
        cnt_w = cnt_w + 1

        for ii in tag_names:
            workspace_frame_updated.at[cnt_t,'Workspace ID'] = x.split('-')[0]
            workspace_frame_updated.at[cnt_t,'Workspace Tag'] = ii['gid']
            workspace_frame_updated.at[cnt_t,'Workspace Tag Name'] = ii['name']
            cnt_t = cnt_t + 1
    ws_frame = pd.DataFrame(columns=['Project ID','Project Name','Status Update Title','Status Update Text','Status Update Created By','Status Update Created At','Status Update Modified At','Status Type','Sections','Workspace ID','Parent Object'])
    for project in projects:
        for proj in project:
            result = client.project_statuses.get_project_statuses_for_project(proj['gid'], {'param': 'value', 'param': 'value'}, opt_pretty=True)
            cnt_pr = 0
            project_frame = pd.DataFrame(columns=['Project ID','Project Name','Status Update Title','Status Update Text','Status Update Created By','Status Update Created At','Status Update Modified At','Status Type','Sections','Workspace ID','Parent Object'])
            for i in result:
                status_id = i['gid']
                status_info = client.status_updates.get_status(status_id, {'param': 'value', 'param': 'value'}, opt_pretty=True)
                project_frame.at[cnt_pr,'Status Update Title'] = status_info['title']
                project_frame.at[cnt_pr,'Status Update Created At'] = status_info['created_at']
                project_frame.at[cnt_pr,'Status Update Created By'] = status_info['created_by']['name']
                project_frame.at[cnt_pr,'Status Update Modified At'] = status_info['modified_at']
                project_frame.at[cnt_pr,'Status Type'] = status_info['status_type']
                project_frame.at[cnt_pr,'Status Update Text'] = status_info['text']
                project_frame.at[cnt_pr,'Parent Object'] = status_info['parent']['name']
                cnt_pr = cnt_pr+1
            ################## Project Sections List ##############################

            if(len(project_frame) == 0):
                cnt_wor = 0
                for (columnName, columnData) in project_frame.iteritems():
                    project_frame.at[cnt_wor,columnName] = ''
            ##################### Adding workspace #####################

            project_frame['Workspace ID'] = [d for d in me['workspaces'] if d['gid'] in proj['workspace']['gid']][0]['gid']
            project_frame['Project Name'] = proj['name']
            project_frame['Project ID'] = proj['gid']

            sections = client.sections.get_sections_for_project(proj['gid'])
            section_name = []
            for i in sections:
                section_name.append(i['name'])

            project_frame['Sections'] = [section_name for _ in range(len(project_frame))]
            ################## Project Team Information ###########################
            ws_frame = pd.concat([ws_frame, project_frame])

    ws_frame = ws_frame.reset_index()

    ws_frame = ws_frame.merge(workspace_frame, how='inner',on = 'Workspace ID')
    workspace_frame_updated = workspace_frame_updated.merge(workspace_frame, how='inner',on = 'Workspace ID')
    goals_frame = goals_frame.merge(workspace_frame, how='inner',on = 'Workspace ID')
    portfolio_frame = portfolio_frame.merge(workspace_frame, how='inner',on = 'Workspace ID')
    task_frame_updated = task_frame_updated.merge(workspace_frame, how='inner',on = 'Workspace ID')
    
    status_update_frame = ws_frame
    status_update_frame = status_update_frame.drop(['index'], axis=1)

    def separating_col_func(data_frame, separation_cols):
        df = 'dataframe_'
        max_cell_length = {}
        for colnames1 in separation_cols.split(','):
            cell_length = []
            data_frame[colnames1] = data_frame[colnames1].fillna("").apply(list)
            for i in range(data_frame.shape[0]):
                cell_length.append(len(data_frame[colnames1][i]))
            max_cell_length[colnames1] = max(cell_length)
            df_0 = df+colnames1
            df_0 = pd.DataFrame([[[] for i in range(max_cell_length[colnames1]-1)] for i in range(data_frame.shape[0])],columns=[colnames1+'_{}'.format(x) for x in range(1, max_cell_length[colnames1])])
            data_frame = pd.concat([data_frame, df_0], axis=1)
            for j in range(data_frame.shape[0]):
                for k in range(len(data_frame[colnames1][j])-1):
                    back_it = data_frame.shape[1]-(k+1)
                    #if (k+1) < len(data_frame[colnames1][j]):
                    data_frame.iloc[j, back_it] = data_frame[colnames1][j][k+1]
                    #data_frame[colnames1+'_'+str(k+1)][j] = data_frame[colnames1][j][k+1]
                    #else:
                    #data_frame[colnames1+'_'+str(k+1)][j] = []
                    print('break52')
                    print(j,',',back_it,',',data_frame[colnames1][j][k+1])
                    print('break55')
                    print(data_frame.iloc[j, back_it])
                if len(data_frame[colnames1][j]) != 0:
                    data_frame[colnames1][j] = data_frame[colnames1][j][0]
        return data_frame
    
    tags_frame = pd.DataFrame(columns=['Workspace ID','Tag ID','Tag Name'])
    tag_list_gid = []
    tag_list_name = []
    cnt_tag = 0
    for x in workspace_list:
        tags_work = client.tags.get_tags_for_workspace(x.split('-')[0], opt_pretty=True)
        for taxgg in tags_work:
            tag_list_gid.append(taxgg['gid'])
            tag_list_name.append(taxgg['name'])
        tags_frame.at[cnt_tag,'Workspace ID'] = x.split('-')[0]
        tags_frame.at[cnt_tag,'Tag ID'] = tag_list_gid
        tags_frame.at[cnt_tag,'Tag Name'] =  tag_list_name
        cnt_tag = cnt_tag+1


    def explode_multiple(df1, list_cols):
        for colnames1 in list_cols:
            df1[colnames1] = df1[colnames1].fillna("").apply(list)
        df1['tmp'] = df1.apply(lambda row: list(zip(*(row[x] for x in list_cols))), axis=1)
        df1 = df1.explode('tmp')
        df1['tmp'] = df1['tmp'].fillna("").apply(list)
        print('check712')
        print(pd.DataFrame(df1['tmp'].tolist(), index=df1.index))
        print('check854')
        print(df1[list_cols])
        df1[list_cols] = pd.DataFrame(df1['tmp'].tolist(), index=df1.index)
        df1.drop(columns='tmp', inplace=True)
        return df1

    def equivalent_col_func(data_frame_local, equivalent_cols):
        cnti = 0
        for i in equivalent_cols.split(':'):
            if ':' in equivalent_cols:
                if cnti == 0:
                    list1 = i.split(',')[:-1]
                    cnti = cnti + 1
                else:
                    list1 = i.split(',')
                    list1.pop(0)
                data_frame_local = explode_multiple(data_frame_local,list1)
                #data_frame_local = data_frame_local.explode(list1)
            else:
                list1 = i.split(',')
                data_frame_local = explode_multiple(data_frame_local,list1)
                #data_frame_local = data_frame_local.explode(list1)
        return data_frame_local

    def flattening(data_frame_local,equivalent_cols, not_flattening_cols):
        for colname, coltype in data_frame_local.dtypes.iteritems():
            if colname not in equivalent_cols.split(',') and colname != 'index' and colname not in not_flattening_cols.split(','):
                print(colname)
                data_frame_local = data_frame_local.explode(colname)
        return data_frame_local
    
    def intersection_cols(data_frame_3,col_args):
        new_equiv_string = ''
        for i in col_args.split(','):
            if i in list(data_frame_3.columns.values):
                new_equiv_string = new_equiv_string+i+','
            elif i == ':':
                new_equiv_string = new_equiv_string+i+','
            else:
                print('Mismatch')
        if len(new_equiv_string) != 0:
            if new_equiv_string[-1] == ',':
                new_equiv_string = new_equiv_string[0:(len(new_equiv_string)-1)]
        return new_equiv_string
    
    workspace_frame_updated = workspace_frame_updated.merge(tags_frame,on='Workspace ID')
    task_frame.to_csv('task_frame_pre.csv')
    sep_cols_task = intersection_cols(task_frame_updated, sep_cols)
    if sep_cols_task != '':
        task_frame_updated = separating_col_func(task_frame_updated, sep_cols_task)
    equiv_cols_task = intersection_cols(task_frame_updated, equiv_cols)
    if equiv_cols_task != '' and equiv_cols_task != ':':
        task_frame_updated = equivalent_col_func(task_frame_updated, equiv_cols_task)
    task_frame_updated = flattening(task_frame_updated, equiv_cols_task, not_flat)

    status_update_frame.to_csv('status_update_frame_pre.csv')
    sep_cols_tag = intersection_cols(status_update_frame, sep_cols)
    if sep_cols_tag != '':
        status_update_frame_updated = separating_col_func(status_update_frame, sep_cols_tag)
    equiv_cols_tag = intersection_cols(status_update_frame, equiv_cols)
    if equiv_cols_tag != '' and equiv_cols_tag != ':':
        status_update_frame_updated = equivalent_col_func(status_update_frame_updated, equiv_cols_tag)
    status_update_frame_updated = flattening(status_update_frame_updated, equiv_cols_tag, not_flat)

    workspace_frame_updated.to_csv('workspace_frame_pre.csv')
    sep_cols_ws = intersection_cols(workspace_frame_updated, sep_cols)
    if sep_cols_ws != '':
        workspace_frame_updated = separating_col_func(workspace_frame_updated, sep_cols_ws)
    equiv_cols_ws = intersection_cols(workspace_frame_updated, equiv_cols)
    if equiv_cols_ws != '' and equiv_cols_ws != ':':
        workspace_frame_updated = equivalent_col_func(workspace_frame_updated, equiv_cols_ws)
    workspace_frame_updated = flattening(workspace_frame_updated, equiv_cols_tag, not_flat)

    goals_frame.to_csv('goals_frame_pre.csv')
    sep_cols_goal = intersection_cols(goals_frame, sep_cols)
    if sep_cols_goal != '':
        goals_frame = separating_col_func(goals_frame, sep_cols_goal)
    equiv_cols_goal = intersection_cols(goals_frame, equiv_cols)
    if equiv_cols_goal != '' and equiv_cols_goal != ':':
        goals_frame = equivalent_col_func(goals_frame, equiv_cols_goal)
    goals_frame = flattening(goals_frame, equiv_cols_goal, not_flat)

    portfolio_frame.to_csv('portfolio_frame_pre.csv')
    sep_cols_port = intersection_cols(portfolio_frame, sep_cols)
    if sep_cols_port != '':
        portfolio_frame = separating_col_func(portfolio_frame, sep_cols_port)
    equiv_cols_port = intersection_cols(portfolio_frame, equiv_cols)
    if equiv_cols_port != '' and equiv_cols_port != ':':
        portfolio_frame = equivalent_col_func(portfolio_frame, equiv_cols_port)
    portfolio_frame = flattening(portfolio_frame, equiv_cols_port, not_flat)

    ################################### Subsetting based on user info ###############################
    if workspace_param != ['None']:
        for workspace_param_iter in workspace_param:
            status_update_frame_updated = status_update_frame_updated[status_update_frame_updated["Workspace Name"] == workspace_param_iter]
            goals_frame = goals_frame[goals_frame["Workspace Name"] == workspace_param_iter]
            portfolio_frame = portfolio_frame[portfolio_frame["Workspace Name"] == workspace_param_iter]
            task_frame_updated = task_frame_updated[task_frame_updated["Workspace Name"] == workspace_param_iter]

    if project_param != ['None']:
        for project_param_iter in project_param:
            status_update_frame_updated = status_update_frame_updated[status_update_frame_updated["Project Name"] == project_param_iter]
            task_frame_updated = task_frame_updated[task_frame_updated["Project Name"] == project_param_iter]

    if task_due_date != ['None']:
        for task_due_date_iter in task_due_date:
            task_frame_updated = task_frame_updated[task_frame_updated["Task-Due Date"] == task_due_date_iter]

    if task_start_date != ['None']:
        for task_start_date_iter in task_start_date:
            task_frame_updated = task_frame_updated[task_frame_updated["Task-Start Date"] == task_start_date_iter]

    task_frame_updated.to_csv('/cnvrg/task_frame.csv',index=False)
    status_update_frame_updated.to_csv('/cnvrg/status_update_frame.csv')
    workspace_frame_updated.to_csv('/cnvrg/workspace_frame.csv',index=False)
    goals_frame.to_csv('/cnvrg/goals_frame.csv',index=False)
    portfolio_frame.to_csv('/cnvrg/portfolio_frame.csv',index=False)
    tags_frame.to_csv('/cnvrg/tags_frame.csv',index=False)

else:
    url = query#'https://app.asana.com/api/1.0/tasks/1202266946298519'
    headers = {'Authorization': "Bearer "+PAT}
    res = requests.get(url, headers=headers)
    custom_op = res.text
    output_df_user = pd.read_json(StringIO(custom_op))

    user_custom_data = pd.DataFrame(columns = output_df_user.index.tolist())
    for i in range(output_df_user.shape[0]):
        for j in range(output_df_user.shape[1]):
            user_custom_data.at[j,output_df_user.index.tolist()[i]] = output_df_user['data'][i]

    user_custom_data.to_csv('custom_data.csv')
