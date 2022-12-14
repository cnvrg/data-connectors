# Monday Connector (Library)
## _cnvrg_

The Monday Connector is a library that extracts data from the monday.com Work OS. The connector extracts all user-accessible boards and workspaces and saves the results in CSV format. If users want to execute a specific query, they can specify it and the connector saves the queried results JSON format.

Click [here](https://github.com/cnvrg/data-connectors/tree/master/monday_connector) for more information on this connector.

## Connector Flow
The following list provides this connector's high-level flow:
- The user provides the `apikey` as an argument or as a cnvrg Environment variable. For the latter, select **Projects** > **Settings** > **Environment** and set the key name as `apikey`. The key provided in the Environment variables takes priority over an argument.
- If the user does not provide a specific query, the connector pulls all boards and workspaces from the account and saves them as `boards.csv` and `workspaces.csv`, respectively. The connector also creates a single CSV file for each board and names it as the board's ID.
- If the user does provide a specific query, the connector executes only the specific query and saves it as `specific.json`.

## Inputs
Monday Connector usage assumes the user has a monday.com account. This library requires the following inputs:
- `--apikey` − Provide the API key associated with the account. More information can be found [here](https://support.monday.com/hc/en-us/articles/360005144659-Does-monday-com-have-an-API-).
- `separation_columns` − Provide the values to be distributed into different columns
- `equivalent_columns` − Provide values to be flattened together
- `not_flatten_columns`− Provide the values to not be distributed into different columns
- `specific_query` − Provide a specific query here if all boards and workspaces are not wanted. For example:
    ```
    { boards (limit:1) {name id description items { name column_values { title text} } } }
    ```
    
## Outputs
- If the user does not provide a specific query, the connector pulls all boards and workspaces from the account and saves them as follows:
  - The connector saves all workspaces and their IDs, names, and descriptions as `workspaces.csv`.
  - The connector saves all boards and their IDs, names, their associated workspace ID, permissions, and owners as `boards.csv`.
  - The connector creates a single CSV file for each board and names it as the board's ID. The CSV file contains all the board's items along with their names, column values, and subitems, if any.
- If the user does provide a specific query, the connector executes only the specific query and saves it as `specific.json`.

## Troubleshooting
Complete one or more of the following steps to troubleshoot issues that may be encountered with this connector:
- Confirm the API key is valid.
- Check the job status, which cnvrg displays simultaneously for each task completed: when the data is pulled and when the job is completed.
- Check the Experiments > Artifacts section to confirm this connector has generated the output CSV files or JSON file.
- Check for an error code, which displays if the experiment fails and cnvrg enters Debug mode, which allows limited time to check the logs in the Experiments tab to resolve the problem.

## Flattening Process
The following table shows an original format:

| col1 | col2 | col3 |
|-|-|-|
|5.4|['abc','xyz']|1,2|

The following tables demonstrate three types of flattening:

### Exploding

| col1 | col2 | col3 |
|-|-|-|
| 5.4 | 'abc' | 1 |
| 5.4 |'abc' | 2 |
| 5.4 | 'xyz' | 1 |
| 5.4 | 'xyz' | 2 |

### Exploding Together

| col1 | col2 | col3 |
|-|-|-|
|5.4|'abc'|1|
|5.4|'xyz'|2|

### Separating

| col1 | col2 | col2a | col3 | col3a |
|-|-|-|-|-|
|5.4|'abc'|'xyz'| 1 | 2 |
