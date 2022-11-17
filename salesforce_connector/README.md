# Salesforce Connector (Library)
The Salesforce Connector is a library that utilizes the Salesforce API to extract customer data based on user inputs. The library then stores this data as a CSV file and provides it as input to existing training and inference blueprints. A Salesforce account, its credentials, and security token are required to use this library.

Click [here](https://github.com/cnvrg/data-connectors/tree/master/salesforce_connector) for more information on this connector.

## Connector Flow
The following list provides this connector's high-level flow:
- The user inputs items such as `username`, `password` and  `security_token` in cnvrg Projects > Settings > Secrets.
- The connector library initiates bulk queries for pulling bulk data from SalesForce, which extracts the data and appends it to a final DataFrame.
- The connector performs each iteration, which utilizes the `data_extraction` function:
    - A `soql` query coupled with a `bulk` query is initiated to pull data from Salesforce.
    - The result is stored in a DataFrame and returned from the function.
- The connector generates the final DataFrame output after it cleans the data based on the `fields_to_get` key.

## Inputs
This library assumes the user has an existing Salesforce account. The Salesforce Connector requires the following inputs:
- `--security_token` − Provide the security token of your Salesforce account. For security reasons, cnvrg recommends creating/updating the cnvrg Secret `????_TOKEN`. Select **Projects** > **Settings** > **Secrets** to store the Salesforce security token.
- `--column_list` − Provide the list of columns from Salesforce to pull. Default Value: `Contact,Account,Order,Lead`.
- `--EntityDefinition_column_list` − List the `EntityDefinition` columns inside the user-defined columns. Default Value: `Id,Name,FirstName,LastName`.
- `--limit`− Set a limit for the number of records to be pulled. Default Value: `None`.
- `--start_date`− Set this parameter to filter the `createdDate` field on the basis of `start_date`. Default Value: `7 days before current date`.
- `--end_date` − Set this parameter to filter the `createdDate` field on the basis of `end_date`. Default Value: `current date`.
- `--keys` − Join multiple tables according to your requirements based on the following `keys`:

  |Account |Contact |Lead |Order |
  |---|---|---|---|
  |Account - Id |Contact - AccountId |Lead - OwnerId |Order - AccountId |
  |Account - ParentId |Contact - OwnerId |Lead - ConvertedAccountId |Order - CreatedById |
  |Account - OwnerId |Contact - CreatedById |Lead - ConvertedContactId | |
  |Account - CreatedById | |Lead - ConvertedOpportunityId | |
  |Account - ParentId | |Lead - CreatedById | |

## Output
- The connector outputs `EntitiyDefination` column data and saves it in `Name_EntityDefinition_Dataframe.csv`.
- The connector writes all files created to the default path `/cnvrg`.
- The user (optionally) requests columns and the library stores the `output.csv` file as a new or existing cnvrg dataset.

## Troubleshooting
Complete one or more of the following steps to troubleshoot issues that may be encountered with this connector:
- Confirm the `security_token` and other parameters are valid.
- Confirm the code prints the job status simultaneously for each task completed: when the data is pulled and when the job is completed.
- Check the Experiments > Artifacts section to confirm this connector has generated the output CSV files.
- Check the logs (in the Experiments tab) for an error message. In the experiment fails, an error displays and cnvrg enters its Debug mode, which provides limited time to review the logs and resolve the problem.

## Related Blueprints
The Salesforce Connector can be used with the following blueprints:
- [Churn Detection Train](https://metacloud.cloud.cnvrg.io/marketplace/blueprints/churn-detection-train)
- [Churn Detection Inference](https://metacloud.cloud.cnvrg.io/marketplace/blueprints/churn-detection-inference)
