# Parameters

- `--auth_token` - string, required. API access token for your Twilio workspace. For security reasons, we recommend creating/updating the Cnvrg Secret `TWIL_TOKEN`
under Project->Settings->Secrets to store the Twilio API token. Enter the value ‘Secret’ if the Cnvrg Secret has been created/updated; otherwise enter the actual API token.
- `--account_sid` - string, required. Client ID for your Twilio workspace. For security reasons, we recommend creating/updating the Cnvrg Secret `TWIL_SID`
under Project->Settings->Secrets to store the Twilio Client ID. Enter the value ‘Secret’ if the Cnvrg Secret has been created/updated; otherwise enter the actual Client ID.
- `--conv_id` - string, required. Conversation ID to be fetched. To find specific conversation ID, refer to [https://www.twilio.com/docs/conversations/api/conversation-resource](https://www.twilio.com/docs/conversations/api/conversation-resource)
- `--leng_limit` - int, optional. Limits the number of messages messages fetched from the most recent. Default value - ‘None’
- `--cnvrg_dataset` - string, optional. Name of the cnvrg dataset to store the csv file. Default value - ‘None’
- `--file_name` - string, optional. Name of the csv file to be generated. Default value - ‘intercom.csv’

# Authentication

This library assumes that the user has an existing Intercom workspace. An API token and client ID can be obtained by creating an app in your workspace. More details on creating an app and authentication can be found [here](https://developers.intercom.com/building-apps/docs/get-started-developing-on-intercom).