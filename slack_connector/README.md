# Slack Connector

The Slack connector is used to get data from the Slack application which can be fed as an input for other blueprints.
The Slack API token of the user and channed id (to pull messages from) are required as input - both of which can be obtained from the user's Slack account.
 
## Parameters:
--channel_id - list, required. Channel id to pull messages from. You can get data from multiple channels (eg: ABC< DEF) by specifying them in the following way: --channel_id ABC DEF
To have your credentials secured, we recommend updating the Cnvrg Secret SLACK_CHANNELID under Project->Settings->Secrets to store the SLACK CHANNEL ID. Enter the value 'Secret' if the Cnvrg Secret is present, otherwise enter the actual Channel ID.

--api_token - string, required. API token for Slack account.  To have your credentials secured, we recommend updating the Cnvrg Secret SLACK_APITOKEN under Project->Settings->Secrets to store the SLACK API token. Enter the value 'secret' if the Cnvrg Secret is present, otherwise enter the actual API token.

--file_name - string, optional. Name of the csv file to be generated. Default - ‘slack.csv’


## Components:
- Based on the authentication scopes provided to the token, we can read and write data from Slack. In this case, we are extracting the conversations history using the slack_sdk module. To get the conversations history, the auth token requires the following scopes: channels:history, groups:history, im:history, mpim:history
- The library stores the output in the form of a csv file with the following headers: type_of_message, text, user, timestamp, subtype
- The extracted output csv file can be used as an input to other Blueprints for training and inference.


## Sample command: 
```
python main.py --channel_id <channel_ids> --api_token <api_token> 
```



