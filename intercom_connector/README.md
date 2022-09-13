# Intercom Connector
## _cnvrg_

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

The Intercom Connector is a library that utilizes the Intercom API to pull data resources (such as conversation IDs, message IDs, and messages) from an Intercom workspace. The library cleans the data (from the API), stores it as a dataset in CSV format, and then feeds it as input to existing model inference and batch predict blueprints. An Intercom workspace, its client ID, and its API access token are required to use this library.

Click [here](https://github.com/cnvrg/data-connectors/tree/master/intercom_connector) for more information on this connector.

## Connector Flow
The following list outlines this connector's high-level flow:
- The user defines inputs such as `api_token` and `client_id` in cnvrg Projects > Settings > Secrets or provides them as arguments. Refer to the [Run Instructions](#run-instructions) later in this documentation.
- The user provides the `start_date` and `end_date` as input arguments to exchange messages during a specific timeframe. The library pulls *all* messages from your workspace in the absence of start and end dates.
- The library performs exception handling and prints descriptive error messages in certain situations. For example, it prints an error message if no messages are exchanged during the input timeframe (start and end dates).
- The library removes HTML syntax and punctuation from the raw text and stores the dataset in CSV format.

## Inputs
This library assumes that the user has an existing Intercom workspace. The user's Intercom API token and client ID are required as input, both of which can be obtained by creating an app in your workspace. More details on creating an app and authentication can be found [here](https://developers.intercom.com/building-apps/docs/get-started-developing-on-intercom).
The Intercom Connector requires the following inputs:
* `--api_token` −  string, required. Provide the API Access Token of your Intercom workspace. For security reasons, cnvrg recommends creating/updating the cnvrg Secret `INT_APITOKEN`. Select **Projects** > **Settings** > **Secrets** to store the Intercom API Access Token. Enter the **Value** `Secret` if the cnvrg Secret has been created/updated; otherwise enter the actual API Access Token.
* `--client_id` − string, required. Provide the Client ID for your Intercom workspace. For security reasons, cnvrg recommends creating/updating the cnvrg Secret `INT_CLIENTID`. Select **Projects** > **Settings** > **Secrets** to store the Intercom Client ID. Enter the **Value** `Secret` if the cnvrg Secret has been created/updated; otherwise enter the actual Client ID.
* `--start_date` − string, optional. Set the start date in `mm/dd/yyyy` format for pulling messages exchanged during a certain timeframe. Default value: `None`.
* `--end_date` − string, optional. Set the end date in `mm/dd/yyyy` format for pulling messages exchanged during a certain timeframe. Default value: `None`.
* `--file_name` − string, optional. Enter a file name to store the CSV file to contain the Intercom data. Default value: `intercom.csv`.
* `--cnvrg_dataset` − string, optional. Provide a name of cnvrg dataset to store the CSV file. Default value: `None`.

## Run Instructions
Refer to the following sample command to run the connector code:

```bash
python intercom_connector.py --api_token <api_token> --client_id <client_id> --start_date 04/28/2022 --end_date 06/28/2022
```
## Outputs
The Intercom Connector generates the following outputs:
- The library outputs a CSV file with the following format: `conversation_id`, `message_id`, `timestamp`, `date`, `message_text`. The following is an example output CSV file:

  |**`convo_id`**|**`message_id`**|**`timestamp`**|**`date`**|**`message_text`**|
  |:-:|:-:|:-:|:-:|:-:|
  |`183402700000095`|`23429202`|`1659438674`|`08/02/2022`|`cb`|
  |`183402700000094`|`23429093`|`1659438477`|`08/02/2022`|`ab`|
  |`183402700000093`|`23428928`|`1659438145`|`08/02/2022`|`hi`|
- The library writes all files created to the default path `/cnvrg`.
- The user (optionally) stores the output CSV file in a new or existing cnvrg dataset.
## Troubleshooting
- Ensure the Intercom workspace, API token, and Client ID are valid.
- Check the experiment's Artifacts section to confirm the connector has generated the output CSV files.
## Related Blueprint Models
The Intercom Connector can be used with the following blueprints:
- [Task Prioritization Batch](https://metacloud.cloud.cnvrg.io/marketplace/blueprints/task-prioritization-batch)
- [Sentiment Analysis Batch](https://metacloud.cloud.cnvrg.io/marketplace/libraries/sentiment-analysis-batch/latest)
- [Topic Modeling Batch]()