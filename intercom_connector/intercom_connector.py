# Copyright (c) 2022 Intel Corporation
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# SPDX-License-Identifier: MIT

import argparse
import html2text
import os
import pandas as pd
import re
from cnvrgv2 import Cnvrg
from datetime import datetime
from ratelimit import limits, sleep_and_retry
from requests import exceptions, Session

# Rate Limits for Intercom API: A maximum of 166 API calls are permitted every 10 seconds
NUM_OF_CALLS = 166
TIME_PERIOD = 10

cnvrg_workdir = os.environ.get("CNVRG_WORKDIR", "/cnvrg")


class NoneMessageError(Exception):
    """Raise if message is None object"""
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "NoneMessageError: html2text cannot clean up None objects. Please ensure the input string is valid!"


class InvalidDatesError(Exception):
    """Raise when date format entered is incorrect or invalid"""
    def __init__(self, start_date, end_date):
        super().__init__(start_date, end_date)
        self.start_date = start_date
        self.end_date = end_date

    def __str__(self):
        return f'InvalidDatesError: Your start date is {self.start_date} and end date is {self.end_date}. Either the start date or end date is missing. Both dates are required to pull messages during a certain timeframe!'


class TimeStampError(Exception):
    """Raise if start time stamp is greater than end timestamp"""
    def __init__(self, start_ts, end_ts):
        super().__init__(start_ts, end_ts)
        self.start_ts = start_ts
        self.end_ts = end_ts

    def __str__(self):
        return f'TimeStampError: End timestamp ({self.start_ts}) should be greater than start timestamp ({self.end_ts}). Check your start and end dates!'


class NoMessagesError(Exception):
    """Raise when no messages are found in the given timeframe"""
    def __init__(self, start_date, end_date):
        super().__init__(start_date, end_date)
        self.start_date = start_date
        self.end_date = end_date

    def __str__(self):
        return f'NoMessagesError: No messages found between {self.start_date} and {self.end_date}. Please enter different start and end dates!'


def parse_parameters():
    """Command line parser."""
    parser = argparse.ArgumentParser(description="""Intercom Connector""")
    parser.add_argument('--api_token', action='store', dest='api_token', required=True, 
                            help="""--- Intercom API Access Token ---""")
    parser.add_argument('--client_id', action='store', dest='client_id', required=True,
                            help="""--- Intercom Client ID ---""")
    parser.add_argument('--start_date', action='store', dest='start_date', required=False, default='None', 
                            help="""--- start date in mm/dd/yyyy format for pulling messages exchanged during a certain timeframe ---""")
    parser.add_argument('--end_date', action='store', dest='end_date', required=False, default='None', 
                            help="""--- end date in mm/dd/yyyy format for pulling messages exchanged during a certain timeframe ---""")
    parser.add_argument('--local_dir', action='store', dest='local_dir', required=False, default=cnvrg_workdir, 
                            help="""--- The path to save the dataset file to ---""")
    parser.add_argument('--cnvrg_dataset', action='store', dest='cnvrg_dataset', required=False, default='None',
                            help="""--- the name of the cnvrg dataset to store in ---""")
    parser.add_argument('--file_name', action='store', dest='file_name', required=False, default='intercom.csv', 
                            help="""--- name of the dataset csv file ---""")
    return parser.parse_args()


def clean_message(msg, html2text_obj):
    """Cleans raw message text.
    
    Removes html artifacts and certain special characters from raw message text.

    Args:
        msg: A string representing raw message text.
        html2text_obj: An html2text.HTML2Text instance

    Raises:
        NoneMessageError: If message is a None object

    Returns:
        A string representing the processed/cleaned message text
    """
    if msg is None:
        raise NoneMessageError()

    output = html2text_obj.handle(msg).strip()
    output = output.replace('\n', '')
    output = output.replace('\t', '')
    output = re.sub(r'[^\w\s]','',output)
    return output


class Intercom:
    """Class to perform Intercom operations
    
    Enables direct calls to the Intercom API and supports pagination and rate limiting.
    Pulls data resources like conversations/messages from Intercom workspace.

    Attributes:
        session: A requests.Session instance.
    """

    def __init__(self, api_token, client_id):
        """Inits Intercom with api token and client id"""
        self.session = Session()
        self.session.auth= (api_token, client_id)

    def handle_errors(self, api_response):
        """Performs error handling for API calls
        
        Raises:
            SystemExit: HTTPError, ConnectionError, Timeout, TooManyRedirects or RequestException.
        """
        try:
            api_response.raise_for_status()
        except exceptions.HTTPError as errh:
            raise SystemExit(errh)
        except exceptions.ConnectionError as errc:
            raise SystemExit(errc)
        except exceptions.Timeout as errt:
            raise SystemExit(errt)
        except exceptions.TooManyRedirects as errd:
            raise SystemExit(errd)
        except exceptions.RequestException as erre:
            raise SystemExit(erre)

    @sleep_and_retry
    @limits(calls=NUM_OF_CALLS, period=TIME_PERIOD)
    def get_first_page_conversations(self):
        """Pulls all conversations on the first page
        
        Makes an API call to the conversations end point and pulls conversation metadata from the first page.
        Follows rate limits set by Intercom.

        Returns:
            response: conversation metadata in json format.
        """
        response = self.session.get('https://api.intercom.io/conversations')
        self.handle_errors(response)
        return response.json()

    @sleep_and_retry
    @limits(calls=NUM_OF_CALLS, period=TIME_PERIOD)
    def get_next_page_conversations(self, next_page_url):
        """Pulls all conversations on the next page
        
        Makes an API call to the conversations end point and pulls conversation metadata from the next page.
        Follows rate limits set by Intercom.

        Args:
            next_page_url: string representing https endpoint for next page.

        Returns:
            response: conversation metadata in json format. Returns None if next_page_url is None/does not exist.
        """
        if next_page_url is None:
            return None
        response = self.session.get(next_page_url)
        self.handle_errors(response)
        return response.json()

    @sleep_and_retry
    @limits(calls=NUM_OF_CALLS, period=TIME_PERIOD)
    def get_single_conversation(self, convo_id):
        """Pulls a single conversation using a unique conversation id.
        
        Makes an API call to the conversations end point and pulls a single conversation using it's unique conversation id.
        Follows rate limits set by Intercom.

        Args:
            convo_id: string representing unique id for a conversation.

        Returns:
            response: conversation metadata in json format.
        """
        response = self.session.get(f"https://api.intercom.io/conversations/{convo_id}")
        self.handle_errors(response)
        return response.json()

    def get_messages(self, start_date, end_date):
        """Pulls messages from conversations in the Intercom workspace
        
        Uses pagination to iterate through all the pages and then pulls messages from individual conversations.
        Users can also pass start and end dates if they want to pull messages exchanged during a certain timeframe.
        All messages are pulled by deafult if no start and end dates are provided. 

        Args:
            start_date: A string representing the start_date in mm/dd/yyyy format for pulling messages in a certain timeframe
            end_date: A string representing the end_date in mm/dd/yyyy format for pulling messages in a certain timeframe

        Raises:
            InvalidDatesError: If one of the dates is missing.
            TimeStampError: If start timestamp is greater than end timestamp
            NoMessagesError: If no messages were exchanged during the given timeframe

        Returns:
            message_data: a dictionary of lists containing strings representing data headers such as conversation id, message id, timestamp, date and message text 
        """
        if not ((start_date == 'None' and end_date == 'None') or (start_date != 'None' and end_date != 'None')):
            raise InvalidDatesError(start_date, end_date)

        is_timeframe = (start_date != 'None' and end_date != 'None')

        if is_timeframe:
            start_format = datetime.strptime(start_date, "%m/%d/%Y")
            end_format = datetime.strptime(end_date, "%m/%d/%Y")
            start_ts = datetime.timestamp(start_format)
            end_ts = datetime.timestamp(end_format)

            if start_ts > end_ts:
                raise TimeStampError(start_ts, end_ts)

        # Make API calls to pull messages from Intercom workspace using pagination and rate limiting
        message_data = {}
        message_data["convo_id"] = []
        message_data["message_id"] = []
        message_data["timestamp"] = []
        message_data["date"] = []
        message_data["message_text"] = []
        
        result = self.get_first_page_conversations()
        next_page = ""

        while next_page is not None:
            for conversation in result["conversations"]:
                convo_id = conversation["id"]
                convo = self.get_single_conversation(convo_id)
                if is_timeframe:
                    first_message_ts = float(convo["created_at"])
                    if first_message_ts >= start_ts and first_message_ts <= end_ts:
                            message_data["convo_id"].append(convo_id)
                            message_data["message_id"].append(convo["source"]["id"])
                            message_data["timestamp"].append(convo["created_at"])
                            message_data["date"].append(datetime.fromtimestamp(first_message_ts).strftime('%m/%d/%Y'))
                            message_data["message_text"].append(convo["source"]["body"])
                else:
                    message_data["convo_id"].append(convo_id)
                    message_data["message_id"].append(convo["source"]["id"])
                    message_data["timestamp"].append(convo["created_at"])
                    message_data["date"].append(datetime.fromtimestamp(float(convo["created_at"])).strftime('%m/%d/%Y'))
                    message_data["message_text"].append(convo["source"]["body"])
                convo_parts = convo["conversation_parts"]["conversation_parts"]
                for part in convo_parts:
                    if is_timeframe:
                        message_ts = float(part["created_at"])
                        if message_ts >= start_ts and message_ts <= end_ts:
                            message_data["convo_id"].append(convo_id)
                            message_data["message_id"].append(part["id"])
                            message_data["timestamp"].append(part["created_at"])
                            message_data["date"].append(datetime.fromtimestamp(message_ts).strftime('%m/%d/%Y'))
                            message_data["message_text"].append(part["body"])
                    else:
                        message_data["convo_id"].append(convo_id)
                        message_data["message_id"].append(part["id"])
                        message_data["timestamp"].append(part["created_at"])
                        message_data["date"].append(datetime.fromtimestamp(float(part["created_at"])).strftime('%m/%d/%Y'))
                        message_data["message_text"].append(part["body"])
            next_page = result["pages"]["next"]
            result = self.get_next_page_conversations(next_page)

        if len(message_data["message_text"]) == 0:
            raise NoMessagesError(start_date, end_date)

        return message_data
    

def main():
    """Command line execution."""
    # Initial setup
    args = parse_parameters()
    if args.api_token.lower() == 'secret':
        args.api_token = os.environ.get('INT_APITOKEN')
    if args.client_id.lower() == 'secret':
        args.client_id = os.environ.get('INT_CLIENTID')
    intercom = Intercom(args.api_token, args.client_id)

    # Pull messages from Intercom Workspace 
    messages_dict = intercom.get_messages(args.start_date, args.end_date)

    # Create a dataframe and remove None entries
    df = pd.DataFrame(messages_dict)
    df.dropna(inplace=True)

    # Preprocess and clean up message text if applicable
    html_convertor = html2text.HTML2Text()
    df["message_text"] = df["message_text"].apply(lambda msg: clean_message(msg, html_convertor))

    # Create a dataset in csv format
    df.to_csv(args.local_dir+'/'+args.file_name, index=False)

    # Store dataset csv as cnvrg dataset
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


if __name__ == "__main__":
    main()