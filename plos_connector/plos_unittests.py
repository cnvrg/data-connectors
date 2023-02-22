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
        """Checks if the URL is valid """
        
        # Provide invalid url
        invalid_url = "https://journals.plos.org/invalid-url"

        
        response = download_journals(invalid_url, self.filename) 

        # Check for status code
        assert response.status_code == 200
        
        # Check if the downloaded file exists
        assert os.path.exists(self.filename)

    def __str__(self):
        return "UrlError: Invalid URL, please provide URL that leads to a downloadable PDF "




class HeaderError(TestPlos):
    def test_header(self):
        """Checks if the header is correct"""

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
        """Checks for network error"""

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
        """Checks if file was downloaded correctly"""
        
        response = download_journals(self.url, self.filename)

        # Check for status code
        assert response.status_code == 200
        
        # Test that the file was downloaded and saved to disk with the correct filename
        assert os.path.exists(self.filename)
        assert os.path.isfile(self.filename)


    def __str__(self):
        return "FileError: File not downloaded correctly "
