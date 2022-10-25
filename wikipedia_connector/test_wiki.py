import unittest
import os
from wiki import WikiPage
from bs4 import BeautifulSoup
import urllib.request
from urllib.request import urlopen
from wiki import WikiPage
import yaml
import pandas
from yaml.loader import SafeLoader
YAML_ARG_TO_TEST = "test_arguments"

class TestWiki(unittest.TestCase):
    @classmethod
    def setUpClass(self) -> None:
        # Parse the wiki page
        cfg_path = os.path.dirname(os.path.abspath(__file__))
        cfg_file = cfg_path + "/" + "test_config.yaml"
        self.test_cfg = {}
        with open(cfg_file) as c_info_file:
            self.test_cfg = yaml.load(c_info_file, Loader=SafeLoader)
        self.test_cfg = self.test_cfg[YAML_ARG_TO_TEST]
        self.wiki = WikiPage(str(self.test_cfg["page"]))

        # Extracting raw text - for 'get_clean_text' argument
        soup = BeautifulSoup(
            urlopen("https://en.wikipedia.org/wiki/" + str(self.test_cfg["page"])).read(), "lxml"
        )
        self.raw_text = ""
        for paragraph in soup.find_all("p"):
            self.raw_text += paragraph.text

        # Setup for testing 'get_wiki_page' and 'get_clean_text' functions
        self.wiki_output = self.wiki.get_wiki_page(str(self.test_cfg["page"]))
        self.processed_text = self.wiki.get_clean_text(self.raw_text)

    def retrieve_first_n_lines(self, n):
        # Pass the number of lines to compare - parameter 'n'
        retrieved_text = self.wiki_output[0]
        lines_split = retrieved_text.lstrip(" ").rstrip(" ").split(".")
        content_lines = ''
        for i in range(n):
            content_lines += lines_split[i] + "."
        return content_lines

    def test_return_type_list(self):
        # Checks if the 'get_wiki_page' function returns list
        self.assertIsInstance(
            self.wiki_output, list
        )

    def test_str_return_type(self):
        # Checks if the list object type is string
        self.assertIsInstance(
            self.wiki_output[0], str
        )

    def test_output_length(self):
        # Checks if the get_wiki_page function returns an output list with length 2
        self.assertEqual(
            len(self.wiki_output), 2
        )

    def test_text_content(self):
        # Checks the content validity for first five lines - from the actual wikipedia page
        self.assertEqual(
            self.retrieve_first_n_lines(5), self.test_cfg["content_val"]
        )

    def test_return_type_str(self):
        # Checks if the 'get_clean_text' function returns string
        self.assertIsInstance(self.processed_text, str)

    # WIP - Develop a test-case to check 'get_clean_text' functionality

if __name__ == "__main__":
    unittest.main()