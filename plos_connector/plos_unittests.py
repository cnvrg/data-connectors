import requests
import requests_mock
import unittest
from plos_main import *


class TestPlos(unittest.TestCase):
    def setUp(self):
        """Overrides setUp from unittest to get dataset for unit testing"""
        
         with open("./config_params.yaml", "r") as file:
            config = yaml.load(file, Loader=yaml.FullLoader)

        # Define paths from config file 

        self.testurl1 = config["url1"]
        self.testfilename1 = config["filename1"]
        self.testurl2 = config["url2"]
        self.testfilename2 = config["filename2"]
        self.invalid_url = config["invalid_url"]



class UrlError(TestPlos):
    def test_url(self):
        """Checks if the URL is valid """
                      
        response = download_journals(self.invalid_url, self.filename) 

        # Check for status code
        self.assertEqual(response.status_code, 200)
        
        # Check if the downloaded file exists
        self.assertTrue(os.path.exists(self.filename))

    def __str__(self):
        return "UrlError: Invalid URL, please provide URL that leads to a downloadable PDF "




class HeaderError(TestPlos):
    def test_header(self):
        """Checks if the header is correct"""

        # Send an HTTP GET request to the PLOS website without the Accept header
        response = requests.get(self.url1)

        # Check if the response was successful (HTTP status code 200)
        self.assertEqual(response.status_code, 200)

        # Test that the response content is a PDF file
        self.assertEqual(response.headers["Content-Type"], "application/pdf")


    def __str__(self):
        return "HeaderError: Response should contain correct file type i.e. 'PDF' "



class NetworkError(TestPlos):
    def test_network(self):
        """Checks for network error"""

        headers = {"Accept": "application/pdf"}
        # Send an HTTP GET request to the PLOS website without the Accept header
        with requests_mock.Mocker() as m:
            m.get(self.url, exc=requests.exceptions.ConnectTimeout)

            response = requests.get(self.url1, headers=headers)

            # Check if the response was successful (HTTP status code not 200)
            self.assertEqual(response.status_code, 200)



    def __str__(self):
        return "NetworkError: Check your connection and newtwork settings "




class FileError(TestPlos):
    def test_file(self):
        """Checks if file was downloaded correctly"""
        
        response1 = download_journals(self.testurl1, self.testfilename1)
        
        response2 = download_journals(self.testurl2, self.testfilename2)

        # Check for status code
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)
        
        
        # Test that the file was downloaded and saved to disk with the correct filename
        self.assertTrue(os.path.exists(self.testfilename1))
        self.assertTrue(os.path.isfile(self.testfilename1))
        
        self.assertTrue(os.path.exists(self.testfilename2))
        self.assertTrue(os.path.isfile(self.testfilename2))



    def __str__(self):
        return "FileError: File not downloaded correctly, please check input parameters "
