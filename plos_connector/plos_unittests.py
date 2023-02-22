import requests
import requests_mock
import unittest
from main import *


class TestPlos(unittest.TestCase):
    def setUp(self):
        """Overrides setUp from unittest to get dataset for unit testing"""

        self.url = "https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0231476&type=printable"
        self.filename = "test_filename.pdf"



class UrlError(TestPlos):
    def test_url(self):
        """Checks if the function returns a float value"""
        invalid_url = "https://journals.plos.org/invalid-url"
        # Send an HTTP GET request to the PLOS website with the Accept header set to "application/pdf"
        headers = {"Accept": "application/pdf"}
        response = requests.get(invalid_url, headers=headers)

        # Check if the response was successful (HTTP status code 200)
        assert response.status_code == 200

        # Check if the downloaded file exists
        assert os.path.exists(self.filename)

    def __str__(self):
        return "UrlError: Invalid URL, please provide URL that leads to a downloadable PDF "




class HeaderError(TestPlos):
    def test_header(self):
        # Send an HTTP GET request to the PLOS website without the Accept header
        response = requests.get(self.url)

        # Check if the response was successful (HTTP status code 200)
        assert response.status_code == 200

        # Test that the response content is a PDF file
        assert response.headers["Content-Type"] == "application/pdf"


    def __str__(self):
        return "HeaderError: Response should contain correct file type i.e. 'PDF' "



class NetworkError(TestPlos):
    def test_network(self):
        headers = {"Accept": "application/pdf"}
        # Send an HTTP GET request to the PLOS website without the Accept header
        with requests_mock.Mocker() as m:
            m.get(self.url, exc=requests.exceptions.ConnectTimeout)

            response = requests.get(self.url, headers=headers)

            # Check if the response was successful (HTTP status code not 200)
            assert response.status_code == 200

            # Test if the file was downloaded and saved to disk
            assert os.path.exists(self.filename)


    def __str__(self):
        return "NetworkError: Check your connection and newtwork settings "




class FileError(TestPlos):
    def test_file(self):
        headers = {"Accept": "application/pdf"}

        response = requests.get(self.url, headers=headers)

        # Check if the response was successful (HTTP status code 200)
        assert response.status_code == 200

        # Save the response content to a file with the custom filename
        with open(self.filename, "wb") as f:
            f.write(response.content)
        # Test that the file was downloaded and saved to disk with the correct filename
        assert os.path.exists(self.filename)
        assert os.path.isfile(self.filename)


    def __str__(self):
        return "FileError: File not downloaded correctly "
