import os
import logging
import argparse
import pandas as pd
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from cnvrgv2 import Cnvrg



#cnvrg_workdir = os.environ.get("CNVRG_WORKDIR", "C:/Users/svelanka/Downloads/Blueprints/slack_connector/slack_connector/")
cnvrg_workdir = os.environ.get("CNVRG_WORKDIR", "/cnvrg")


class NoMessageError(Exception):
    """Raise if no messages are obtained"""
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "NoMessageError: No messages obtained from this channel. Please ensure that channel contains messages."


class HeadersMismatchError(Exception):
    """Raise if headers are not in correct format"""
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "HeadersMismatchError: Required headers not obtained from messages dictionary. Please ensure data is in correct format."




def get_parameters():
    
    parser = argparse.ArgumentParser(description="Slack Connector")
    parser.add_argument('--api_token', action='store', dest='api_token', required=True, 
                            help="Slack API Access Token")
    parser.add_argument('--channel_id', nargs='+', action='store', dest='channel_id', required=True, 
                            help="Slack channel ID")
    parser.add_argument('--local_dir', action='store', dest='local_dir', required=False, default=cnvrg_workdir, 
                            help="""--- The path to save the dataset file to ---""")
    
    parser.add_argument('--cnvrg_dataset', action='store', dest='cnvrg_dataset', required=False, default='None',
                            help="""--- the name of the cnvrg dataset to store in ---""")
    parser.add_argument('--file_name', action='store', dest='file_name', required=False, default="slack.csv", 
                            help="""--- name of the dataset csv file ---""")
    
    return parser.parse_args()




def get_messages(api_token,channel_id):
        
        
        """Pulls messages from a Slack channel using input api token and unique channel id
        
    Makes an API call to get messages from Slack

    Args:
            api_token: string representing unique authentication token from user
            channel_id: unique channel ID in string format

    Returns:
            conversation_history: conversation metadata as dataframe
        """
        
        client = WebClient(token=api_token)
        logger = logging.getLogger(__name__)
        conversation_history = []
        df = []

        for c in channel_id:

            try:

                result = client.conversations_history(channel = c)
                conversation_history = result["messages"]
                

                if conversation_history.empty == True:
                    raise NoMessageError()

                df_conversation_history = pd.DataFrame(conversation_history)
                df.append(df_conversation_history)
            
            except SlackApiError as e:

                if e.response.data.get("error", "") == "not_in_channel":
               
                    logger.warning('Attempted to get messages for channel: {} that '
                    'user is not in'.format(c))

                    conversation_history = None
            
                else:
                    logger.error("Error creating conversation list: {}".format(e))
                    raise e
            
                        

        df = pd.concat(df)
        
        return df
    

def filter_data(df):

    """ Filters data from Slack
    
    Removes unwanted column from dataframe and saves dataframe in csv format

    Args:
        df: Dataframe containing raw messages
      
    Returns:
        A dataframe with processed columns
    """

    # Filter dataframe to keep required columns
    df = df[['type','text','user','ts','client_msg_id','subtype']]

    # Raise error if datframe is empty
    if df.empty == True:
        raise NoMessageError()

    list1 = list(df.columns)
    list2 = ['type','text','user','ts','client_msg_id','subtype']
    difference_set = set(list1)-set(list2)

    # Raise error if all required headers are imported
    if difference_set != set():
            raise HeadersMismatchError()
    
 

    return df




def main():
    """Command line execution"""

    # Get parameters
    args = get_parameters()
    if args.api_token.lower() == 'secret':
        args.api_token = os.environ.get('SLACK_APITOKEN')
    if args.channel_id == 'secret':
        args.channel_id = os.environ.get('SLACK_CHANNELID')

    
    # Pull messages from Slack channel 
    messages_dict = get_messages(args.api_token,args.channel_id)

    # Create a dataframe 
    df = pd.DataFrame(messages_dict)

    # Filter data
    df = filter_data(df)
    
    # Create csv file
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

        
