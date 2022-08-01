# Asana Connector
## _cnvrg_

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

This connector extracts data from Asana accounts, filtering based on user inputs. The Data that is extracted needs further processing to make it suitable for attaching alongside other blueprints, like Churn Prediction or Sentiment Analysis

## Input
- `access_token`: asana personal access token .
    **Default Value -** <your_access_token>
- `workspace`: workspace name that the user wants to filter data on.
    **Default Value -** <your_workspace_name>
- `project`: project name that the user wants to filter data on.
    **Default Value -** <your_project_name>
-	`query`: If the user wants to write a custom query rather than use default table that comes as output
    **Default Value -** https://app.asana.com/api/1.0/tasks/XXXXXXXXXXXXX
-	`task_start_date`: filter data on the range of dates between which, a task could have started
    **Default Value -** YYYY-MM-DD,Y1Y1Y1Y1-M1M1-D1D1
-	`task_due_date`: filter data on the range of dates between which, a task could have ended
    **Default Value -** YYYY-MM-DD,Y1Y1Y1Y1-M1M1-D1D1
-   `premium_account`: whether you have a premium asana account or not
    **Default Value -** No
-   `separation_columns`: values which need to distributed into different columns
    **Default Value -** "Sub-Task Attachment,Team Name"
-   `equivalent_columns`:values which need to be flattened together
    **Default Value -** Task-Comment Gid,Task-Comment Created At,Task-Comment Text,Task-Comment Created By,Task-Comment Resource SubType,:,Sub-Task Comment Gid,Sub-Task Comment Created At,Sub-Task Comment Text,Sub-Task Comment Created By,Sub-Task Comment Resource Subtype
-   `not_flatten_columns`: values which don't need to distributed into different columns
    **Default Value -** "Tag-ID, Tag Name"
    

## Code Flow
- User inputs such as: **access token** needs to be defined in _environment_  tab on the cnvrg platform
- Bulk queries for pulling data in bulk from salesforce are initiated which pulls the data which is appended to a final dataframe
- Eventually, the lists in the data are exploded to create strings from lists (and thus increasing the number of rows)
- A total of 6 dataframes are created, workspace/tag/task/goals/project and portfolio. Some of them are found in only premium accounts (like goals and portfolios)
## Joining Tables
- User can join multiple tables according to their requirement based on following `keys`

|Task |Tag |Workspace |Project |Portfolio| Goals
|---|---|---|---|---|---|
|Workspace ID |Project ID |Workspace ID |Project ID |Workspace ID|Workspace ID 

## Output
-   task_frame.csv` [Tasks/Sub-tasks related data]`
-   status_update_frame `[tags related data]`
-   goals_frame.csv ` [Premium feature, goals]`
-   workspace_frame.csv ` [basic workspace info]`
-   portfolio_frame.csv ` [Premium feature, portfolio]`

## How to run
```
python3 asana/asana1.py --access_token 1/1202266991680810:8378229ef7d219bc520cae6c8a69ed73 --workspace "None" --project "None" --query "None" --task_start_date "None" --task_due_date "None" --premium_account No --equivalent_columns "Task-Comment Gid,Task-Comment Created At,Task-Comment Text,Task-Comment Created By,Task-Comment Resource SubType,:,Sub-Task Comment Gid,Sub-Task Comment Created At,Sub-Task Comment Text,Sub-Task Comment Created By,Sub-Task Comment Resource Subtype" --separation_columns "Sub-Task Attachment,Team Name" --not_flatten_columns "Tag-ID, Tag Name" 
```
## Flattening Process
Flattening essentially is of 3 types, described below.

Original Table

| col1 | col2 | col3 |
|-|-|-|
|5.4|'abc','xyz'|1,2|

Exploding

| col1 | col2 | col3 |
|-|-|-|
| 5.4 | 'abc' | 1 |
| 5.4 |'abc' | 2 |
| 5.4 | 'xyz' | 1 |
| 5.4 | 'xyz' | 2 |

Exploding Together

| col1 | col2 | col3 |
|-|-|-|
|5.4|'abc'|1|
|5.4|'xyz'|2|

Separating

| col1 | col2 | col2a | col3 | col3a |
|-|-|-|-|-|
|5.4|'abc'|'xyz'| 1 | 2 |

## References
[Asana query sample](https://developers.asana.com/docs/get-tags-in-a-workspace)
[Asana Docs](https://developers.asana.com/docs/)
[Asana App (website)](https://app.asana.com/)