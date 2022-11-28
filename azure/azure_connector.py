from cnvrgv2 import Cnvrg
from datetime import datetime
import os
import argparse
from azure.storage.blob import ContentSettings, ContainerClient
import logging

class azure:
    def __init__(self, args, container_name=None):
        """
        Try to initialise container service using either connection string or account url.
        Connection string can be either provided as an argument or environment key.
        Environment key string will override the argument string.
        If the account url provided is None, intialisation will be done using conn str
        else it will be done using account url.
        """
        self.cnvrg_workdir = os.environ.get("CNVRG_WORKDIR", "/cnvrg")
        self.container_name = args.container_name
        self.account_url = args.account_url
        self.conn_str = args.conn_str
        try:
            self.conn_str = os.environ['CONN_STRING']
        except KeyError:
            logging.info("Connection string is not provided in the environment keys")  
            
        if self.account_url is None:
            self.containerservice = ContainerClient.from_connection_string(
                conn_str=self.conn_str, container_name=self.container_name
            )
        else:
            self.containerservice = ContainerClient(account_url=self.account_url, container_name=self.container_name)
        self.all_blobs = []

    def save_blob(self, file_name):
        # Get full path to the file
        download_file_path = os.path.join(self.cnvrg_workdir, file_name)
        self.all_blobs.append(download_file_path)
        # for nested blobs, create local path as well!
        os.makedirs(os.path.dirname(download_file_path), exist_ok=True)

        with open(download_file_path, "wb") as my_blob:
            bytes = (
                self.containerservice.get_blob_client(file_name)
                .download_blob()
                .readall()
            )
            my_blob.write(bytes)

    def download_all_blobs_in_container(self):
        my_blobs = self.containerservice.list_blobs()
        for blob in my_blobs:
            self.save_blob(blob.name)


# args
def argument_parser():
    parser = argparse.ArgumentParser(description="""Creator""")
    parser.add_argument(
        "--container_name",
        action="store",
        dest="container_name",
        required=True,
        help="""name of the container you want to download""",
    )
    parser.add_argument(
        "--conn_str",
        action="store",
        dest="conn_str",
        default=None,
        required=False,
        help="""The connection string to your storage account can be found in the Azure Portal under the "Access Keys" section""",
    )
    parser.add_argument(
        "--account_url",
        action="store",
        dest="account_url",
        default=None,
        required=False,
        help="""Enter the account url if anonymous read access is enabled on the container.""",
    )
    return parser.parse_args()


# function to save to cnvrg dataset
def save_to_cnvrg(files_list):
    cnvrg = Cnvrg()
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    ds_name = f"container_{now}"
    ds = cnvrg.datasets.create(name=ds_name)
    ds.put_files(paths=files_list)


# main
def main():
    args = argument_parser()
    azure_downloader = azure(args)
    azure_downloader.download_all_blobs_in_container()
    save_to_cnvrg(azure_downloader.all_blobs)


if __name__ == "__main__":
    main()
