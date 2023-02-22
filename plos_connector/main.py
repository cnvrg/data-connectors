import requests
import os
import argparse


cnvrg_workdir = os.environ.get("CNVRG_WORKDIR", "/cnvrg")

class ValueMismatchError(Exception):
    """Raise if number of urls and filenames do not match"""
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "ValueMismatchError: The number of custom filenames must match the number of URLs."
        

class InvalidUrlError(Exception):
    """Raise if URL is invalid"""
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "InvalidUrlError: Failed to download from given URL, please check if provided URL leads to a downloadable PDF file."
        



def get_parameters():

    parser = argparse.ArgumentParser(description="PLOS Connector")

    parser.add_argument(
        "--urls",
        nargs="+",
        action="store",
        dest="urls",
        required=True,
        help="--- URLs to download journals from ---",
    )

    parser.add_argument(
        "--filenames",
        nargs="+",
        action="store",
        dest="filenames",
        required=False,
        default="j.pdf",
        help="""--- Custom names of the pdf files ---""",
    )
    parser.add_argument(
        "--local_dir",
        action="store",
        dest="local_dir",
        required=False,
        default=cnvrg_workdir,
        help="""--- The path to save the dataset file to ---""",
    )

    parser.add_argument(
        "--cnvrg_dataset",
        action="store",
        dest="cnvrg_dataset",
        required=False,
        default="None",
        help="""--- the name of the cnvrg dataset to store in ---""",
    )

    return parser.parse_args()



def download_journals(urls, filenames=None):

    """Pulls journals as pdf files from a PLOS journal and saves them in the current directory
        
    
    Args:
            urls: string representing unique url(s) for journals to be downloaded
            filenames: string representing names of the files to be provided for downloaded journals

    Downloads:
            Journals in pdf format
        """

    if filenames is not None and len(filenames) != len(urls):
        raise ValueMismatchError()
            
    for i, url in enumerate(urls):
        # Send an HTTP GET request to the PLOS website with the Accept header set to "application/pdf"
        headers = {"Accept": "application/pdf"}
        response = requests.get(url, headers=headers)

        # Check if the response was successful (HTTP status code 200)
        if response.status_code == 200:
            # Extract the filename from the Content-Disposition header, if available
            if "Content-Disposition" in response.headers:
                default_filename = (
                    response.headers["Content-Disposition"]
                    .split("filename=")[-1]
                    .strip()
                )
            else:
                # If the Content-Disposition header is not available, use the URL to generate a filename
                default_filename = url.split("/")[-1]
            # Use the custom filename if provided, otherwise use the default filename
            if filenames is not None:
                save_file = os.path.join(".", filenames[i])
            else:
                save_file = os.path.join(".", default_filename)
            # Save the PDF file to disk
            with open(save_file, "wb") as f:
                f.write(response.content)
        else:
            raise InvalidUrlError()


def main():
    args = get_parameters()
    
    """ testing
    urls = [
    "https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0231476&type=printable",
    "https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0231477&type=printable",
    "https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0231478&type=printable",
    ]
    filenames = ["journal1.pdf", "journal2.pdf", "journal3.pdf"]
    """
    
    download_journals(args.urls, args.filenames)


if __name__ == "__main__":
    main()
