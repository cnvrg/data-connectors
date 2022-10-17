from curses.ascii import isdigit
import os
import argparse
import pandas as pd
from ratelimit import limits, sleep_and_retry
from collections import defaultdict
from cnvrgv2 import Cnvrg
from twilio.rest import Client

# The rate limit based on Twilio's rate of dequeueing messages
# For details, refer to https://support.twilio.com/hc/en-us/articles/115002943027-Understanding-Twilio-Rate-Limits-and-Message-Queues#h_01F0265SAZ9BYNPG0AQZ0AKRHZ
NUM_OF_CALLS = 3
TIME_PERIOD_SEC = 1

cnvrg_workdir = os.environ.get("CNVRG_WORKDIR", "/cnvrg")

def parse_parameters():
    """Command line parser."""
    parser = argparse.ArgumentParser(description="""Twilio Connector""")
    parser.add_argument('--auth_token', action='store', dest='auth_token', required=True, 
                            help="""--- Twilio API Access Token ---""")
    parser.add_argument('--account_sid', action='store', dest='account_sid', required=True,
                            help="""--- Twilio Account SID ---""")
    parser.add_argument('--conv_id', action='store', dest='conv_id', required=True,
                        help="""--- Twilio Conversation ID ---""")
    parser.add_argument('--leng_limit', action='store', dest='leng_limit', required=False, default=None, 
                            help="""--- limit the number of messages fetched from the most recent ---""")
    parser.add_argument('--local_dir', action='store', dest='local_dir', required=False, default=cnvrg_workdir, 
                            help="""--- The path to save the dataset file to ---""")
    parser.add_argument('--cnvrg_dataset', action='store', dest='cnvrg_dataset', required=False, default='None',
                            help="""--- the name of the cnvrg dataset to store in ---""")
    parser.add_argument('--file_name', action='store', dest='file_name', required=False, default='twilio.csv', 
                            help="""--- name of the dataset csv file ---""")
    return parser.parse_args()

class Twilio:

    def __init__(self, auth_token, account_sid):
        self.client = Client(account_sid,auth_token)

    @sleep_and_retry
    @limits(calls=NUM_OF_CALLS, period=TIME_PERIOD_SEC)
    def create_conversation(self, conv_name):
        """Create a new conversation which will be used for data pulling
        Args:
            conv_name: string representing name of the conversation
        Returns:
            conversation: new instance of conversation in Twilio
        """
        self.conversation = self.client.conversations \
                     .v1 \
                     .conversations \
                     .create(friendly_name = conv_name)

        return self.conversation

    @sleep_and_retry
    @limits(calls=NUM_OF_CALLS, period=TIME_PERIOD_SEC)
    def add_message(self, conv_id, author, message):
        """Add a new message in the conversation 
        Args:
            conv_id: string representing unique id of of the conversation
            author: string representing the author of the message
            message: string representing the body of the message
        Returns:
            
        """
        self.conversation = self.client.conversations \
                .v1 \
                .conversations(conv_id) \
                .messages \
                .create(author=author, body=message)

        return None

    @sleep_and_retry
    @limits(calls=NUM_OF_CALLS, period=TIME_PERIOD_SEC)
    def get_conversation(self, conv_id, leng_limit=None):
        """Pulls a conversation messages using a unique conversation id from most recent.
        
        Makes an API call to the conversations end point and pulls a single conversation using it's unique conversation id.
        Follows rate limits set by Twilio.
        Args:
            conv_id: string representing unique id for a conversation.
            leng_limit: limit the number of messages fetched from the most recent
        Returns:
            messages: list of conversation message instances
        """
        if leng_limit is not None and leng_limit.isdigit():
            leng_limit = int(leng_limit)
            self.messages = self.client.conversations \
                                .v1 \
                                .conversations(conv_id) \
                                .messages \
                                .list(order='desc', limit=leng_limit)
        else:
            self.messages = self.client.conversations \
                    .v1 \
                    .conversations(conv_id) \
                    .messages \
                    .list(order='desc')
        return self.messages

def main():
    args = parse_parameters()
    if args.auth_token.lower() == 'secret':
        args.auth_token = os.environ.get('TWIL_TOKEN')
    if args.account_sid.lower() == 'secret':
        args.account_sid = os.environ.get('TWIL_SID')
    twilio = Twilio(args.auth_token, args.account_sid)
    messages = twilio.get_conversation(args.conv_id, args.leng_limit)
    messages_map = defaultdict(list)

    # for msg in messages:
    #     print(msg.date_created)
    #     print(msg.author)
    #     print(msg.body)

    for msg in messages:
        messages_map['date_created'].append(msg.date_created)
        messages_map['author'].append(msg.author)
        messages_map['body'].append(msg.body)

    df = pd.DataFrame(messages_map)
    df.dropna(inplace=True)
    df.to_csv(args.local_dir+'/'+args.file_name, index=False)

    # Store twilio csv as cnvrg dataset
    if args.cnvrg_dataset.lower() != 'none':
        cnvrg = Cnvrg()
        ds = cnvrg.datasets.get(args.cnvrg_dataset)
        try:
            ds.reload()
        except:
            print("The provided Dataset was not found")
            print(f"Creating a new dataset named {args.cnvrg_dataset}")
            ds = cnvrg.datasets.create(name=args.cnvrg_dataset)
        print("Uploading files to Cnvrg dataset")
        os.chdir(args.local_dir)
        ds.put_files(paths=[args.file_name])


if __name__ == '__main__':
    main()

