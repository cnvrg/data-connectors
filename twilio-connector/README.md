This library is made to download datasets from twilio

## Finding the dataset name
To grab a dataset name from twilio, navigate into your desired dataset page on twilio, afterwards copy the dataset name from the end of the url.
Paste the twilio dataset name into the `twilio_dataset_name` field.

## Authentication

You can get your twilio API credentials by going into the user profile and under "Account" press "Create API Token".

This will download a "twilio.json" file with your credentials.

It is recommended to use environment variables as authentication method. This library expects the following env variables:
    
* `TWILIO_KEY` - The twilio API key
* `TWILIO_USERNAME` - The twilio API username

The environment variables can be stored securely in the project secrets in cnvrg. 

## Conversations

The Twilio conversation will be downloaded in the following json format:

{
  "sid": "CHXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
  "account_sid": "ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
  "chat_service_sid": "ISXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
  "messaging_service_sid": "MGXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
  "friendly_name": "My First Conversation",
  "unique_name": "unique_name",
  "attributes": {
    "topic": "feedback"
  },
  "date_created": "2015-12-16T22:18:37Z",
  "date_updated": "2015-12-16T22:18:38Z",
  "state": "inactive",
  "timers": {
    "date_inactive": "2015-12-16T22:19:38Z",
    "date_closed": "2015-12-16T22:28:38Z"
  },
  "bindings": {},
  "url": "https://conversations.twilio.com/v1/Conversations/CHXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
  "links": {
    "participants": "https://conversations.twilio.com/v1/Conversations/CHXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/Participants",
    "messages": "https://conversations.twilio.com/v1/Conversations/CHXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/Messages",
    "webhooks": "https://conversations.twilio.com/v1/Conversations/CHXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/Webhooks"
  }
}


