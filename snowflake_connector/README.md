# Snowflake Connector (Library)
The Snowflake Connector enables users to connect to a Snowflake account, run queries, and analyze results. The connector also enables users to pull data from the Snowflake application, create CSV files and DataFrames, and store them as versioned cnvrg datasets. The Snowflake Connector is supported in both cnvrg Flows and Python environments.

Click [here](https://github.com/cnvrg/data-connectors/tree/master/snowflake_connector) for more information on this connector.

## Connector Flow
The following list provides this connector's high-level flow:
- The user runs the following command to install this Python prerequisite (if not already installed): `pip install snowflake-connector-python`
- The user defines inputs such as username and password in cnvrg Projects > Settings > Environment or provides them as arguments. Refer to the [Run Instructions](#run-instructions) section later in this document.
- The user accesses the Snowflake account.
- The Snowflake Connector (with the username and password passed as Environment variables) pulls the Snowflake data, creates CSV files and DataFrames, and stores them as versioned cnvrg datasets.

## Inputs
This library assumes the user has an existing Snowflake account (to pull data from). The user's Snowflake username and password are required as input, both of which can be obtained from the user's Snowflake account.

The Snowflake Connector requires the following inputs:
### Executable Parameters
* `--query` (string, required) - the Snowflake query to be executed
* `--output_file` (string, optional) - the filename to store the query as a CSV file
### Configuration Parameters
* `--warehouse` - Snowflake warehouse name
* `--account` - Snowflake account name
* `--database` - Snowflake database name
* `--schema` - Snowflake schema name
### Authentication Credentials
The username and password credentials can be passed as arguments. To ensure security, however, the cnvrg team recommends using Environment variables as the authentication method. Go to cnvrg **Projects** > **Settings** > **Environment** to set the following variables:
* `SNOWFLAKE_USER` - account username
* `SNOWFLAKE_PASSWORD` - user account password

::: tip NOTE
The cnvrg Project Settings area securely stores the Environment variables.
:::

 Additionally, you can set the following additional parameters as Environment variables rather than passing them as arguments:
* `SNOWFLAKE_WAREHOUSE` - warehouse name
* `SNOWFLAKE_ACCOUNT` - account username

## Run Instructions
This section provides instructions to perform various Snowflake functions.
### Load the Library
Run the following code to load the connector:
```
from cnvrg import Library
library = Library('cnvrg/snowflake_connector')
library.load()
```
### Connect to the Data Source
Run the following code to connect to your data source:
```
library.connect(warehouse="SNOWFLAKE_WAREHOUSE",
                account="SNOWFLAKE_ACCOUNT",
                database="SNOWFLAKE_DATABASE",
                schema="SNOWFLAKE_SCHEMA")
```
::: tip NOTE
The cnvrg team recommends storing credentials as cnvrg Environment variables.
:::

### Execute a Query
Run the `library.query(query)` code to return a cursor object for later use to retrieve the relevant results:
```
results = library.query("SELECT * FROM users")
results.fetchall()
```
### Load as a CSV/DataFrame
Run the following code to perform a query and automatically retrieve it as DataFrame/CSV file:
```
# Create a dataframe from query in a single line
df = library.to_df("SELECT * FROM users")
```
### Create a CSV File with the Results
Run the following command to create a CSV file containing the results (with the given filename path):
```
library.to_csv("SELECT * FROM users","results.csv")
```
### Close the Connection
Run the following command to close the connection:
```
library.close_connection()
```
## Outputs
The Snowflake Connector library generates the following outputs:
- The connector library outputs a CSV/DataFrame file.
- The library writes all files created to the default path `/cnvrg`.
- The user (optionally) stores the output CSV file in a new or existing cnvrg dataset.

## Troubleshooting
Complete one or more of the following steps to troubleshoot issues that may be encountered with this connector:
- Confirm the username and password are correct and valid.
- Check the experiment's Artifacts section to confirm the connector has generated the output CSV files.
- Check the job status, which cnvrg displays simultaneously for each task completed: when the data is pulled and when the job is completed.
- Check for an error message, which displays if the experiment fails. If so, cnvrg goes into Debug mode, which allows limited time to check the logs in the Experiments tab to resolve the problem.

## Related Blueprint Models
The Snowflake Connector can be used with any blueprint that uses tabular data, such as the following:
- [Anomaly Detection Train](https://app.af2jdjq262tdqvyelihtqnd.cloud.cnvrg.io/blueprintsdev/blueprints/blueprints/anomaly-detection-train)
- [Churn Detection Train](https://app.af2jdjq262tdqvyelihtqnd.cloud.cnvrg.io/blueprintsdev/blueprints/blueprints/churn-detection-train)
- [Recommenders Train](https://app.af2jdjq262tdqvyelihtqnd.cloud.cnvrg.io/blueprintsdev/blueprints/blueprints/recommenders-train)
- [NCF Recommender Train](https://app.af2jdjq262tdqvyelihtqnd.cloud.cnvrg.io/blueprintsdev/blueprints/blueprints/ncf-recommender-train)
