# Pulling data from Monday
## _cnvrg_

This connector extracts data from Monday.com. We extract all boards and workspaces to which the user has access to and save the results in .csv format. In case the user wants to execute a specific query, they specify it and the results for this query will be saved in .json format.

## Input
- `--apikey`: It is the api key associated with the account. Learn about it [here.](https://support.monday.com/hc/en-us/articles/360005144659-Does-monday-com-have-an-API-)
- `specific_query`: In case you don't want the results from all boards and workspaces, you can provide a specific query here. For example:
    ```
    { boards (limit:1) {name id description items { name column_values { title text} } } }
    ```
-   `separation_columns`: values which need to distributed into different columns
-   `equivalent_columns`:values which need to be flattened together
-   `not_flatten_columns`: values which don't need to distributed into different columns

## Code Flow
- User has the option to provide the *apikey* either through argument or set it in the environment variables with key name as *apikey*. The key provided in the environment variables takes priority.
- If the user does not provide a specific query, the connector will pull all boards and workspaces from the account and save them as follows:
    1. All workspaces their ids, names and descriptions will be saved as **workspaces.csv**
    2. All boards their ids, names, workspace id they are associated with, permission and owners as **boards.csv**
    3. For each board a single csv will be created with the name as id of that board. The csv will contain all the items in that board along with their names, column values and subitems if any.
- If the user provides a specific query, only the specific query will be executed and saved as **specific.json**


## Error Handling
-   In case the code is ran successfully, the status and the logs can be checked in the experiment tab. 
-   The code prints the job status simultaneously for each task completed
    - when the data is pulled
    - when the job is completed.
-  In case of an error, the experiment fails, the code gets into debug mode and the logs display the error msg.

## Flattening Process
Flattening essentially is of 3 types, described below.

Original Table

| col1 | col2 | col3 |
|-|-|-|
|5.4|['abc','xyz']|1,2|

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
