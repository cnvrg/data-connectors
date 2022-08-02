# Intercom Connector
## _cnvrg_

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

Intercom Connector is a library that utilizes the Intercom API to pull data resources (conversation ids, message ids, messages) from your Intercom workspace. A client ID and API access token are required to use this library. The data (from the API) is cleaned and stored in a csv file.

## Parameters

* ```--api_token``` - string, required. API access token for your Intercom workspace. For security reasons, we recommend creating/updating the Cnvrg Secret ```INT_APITOKEN``` under Project->Settings->Secrets to store the Intercom API token. Enter the value 'Secret' if the Cnvrg Secret has been created/updated; otherwise enter the actual API token.
* ```--client_id``` - string, required. Client ID for your Intercom workspace. For security reasons, we recommend creating/updating the Cnvrg Secret ```INT_CLIENTID``` under Project->Settings->Secrets to store the Intercom Client ID. Enter the value 'Secret' if the Cnvrg Secret has been created/updated; otherwise enter the actual Client ID.
* ```--start_date``` - string, optional. Start date in mm/dd/yyyy format for pulling messages exchanged during a certain timeframe. Default value - 'None'
* ```--end_date``` - string, optional. End date in mm/dd/yyyy format for pulling messages exchanged during a certain timeframe. Default value - 'None'
* ```--cnvrg_dataset``` - string, optional. Name of the cnvrg dataset to store the csv file. Default value - 'None'
* ```--file_name``` - string, optional. Name of the csv file to be generated. Default value - 'intercom.csv' 

## Authentication

This library assumes that the user has an existing Intercom workspace.
An API token and client ID can be obtained by creating an app in your workspace.
More details on creating an app and authentication can be found [here](https://developers.intercom.com/building-apps/docs/get-started-developing-on-intercom)

## Features

* The library can extract the API token and Client ID from Cnvrg Secrets. This feature can be used by passing the value 'Secret' to ```--api_token``` and/or ```--client_id```.
* Messages exchanged during a specific timeframe can be pulled by providing the start date and end date as input arguments. The library pulls all messages from your workspace in the absence of start and end dates.
* The library performs exception handling and prints descriptive error messages in certain situations. For example, an error message is printed if no messages were exchanged during the input timeframe (start and end dates)
* HTML syntax and punctuation is removed from raw message text.
* An ouptut csv file is generated with the following format: conversation_id, message_id, timestamp, date, message_text.
* The output csv file can also be stored in a new or existing cnvrg dataset.
* All files created by this library are written to the default path '/cnvrg'.

## How to run

Here is a sample command to run this library:

```bash
python intercom_connector.py --api_token <api_token> --client_id <client_id> --start_date 04/28/2022 --end_date 06/28/2022
```