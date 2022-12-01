import unittest
import wikipedia
import os, shutil
from wiki import WikiPage, wiki_main, parse_topic
from bs4 import BeautifulSoup
import urllib.request
from urllib.error import HTTPError
from urllib.request import urlopen
from wiki import WikiPage
import yaml
import pandas
from yaml.loader import SafeLoader
YAML_ARG_TO_TEST = "test_arguments"

class TestWiki(unittest.TestCase):
    @classmethod
    def setUpClass(self) -> None:
        ''' Function used to set up unittesting parameters '''
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

        # Make a Unit-testing data directory    
        self.unittest_dir = "unit_test_data"
        self.local_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_path = os.path.join(self.local_dir, self.unittest_dir)
        os.mkdir(self.data_path)

        # Parsing incorrect arguments
        self.incorrect_flag, self.incorrect_topics = parse_topic(str(self.test_cfg["blank_page"]))

    @classmethod
    def tearDownClass(self):
        shutil.rmtree(self.data_path)

    def retrieve_first_n_lines(self, n):
        ''' Helper function used to retrieve first 'n' lines of wikipedia page content '''
        retrieved_text = self.wiki_output[0]
        lines_split = retrieved_text.lstrip(" ").rstrip(" ").split(".")
        content_lines = ''
        for i in range(n):
            content_lines += lines_split[i] + "."
        return content_lines

    def test_return_type_list(self):
        ''' Checks return type of the 'get_wiki_page' function '''
        self.assertIsInstance(
            self.wiki_output, list
        )

    def test_str_return_type(self):
        ''' Checks the list object type '''
        self.assertIsInstance(
            self.wiki_output[0], str
        )

    def test_output_length(self):
        ''' Checks the output length '''
        self.assertEqual(
            len(self.wiki_output), 2
        )

    def test_text_content(self):
        ''' Checks the validity of the content pulled from wikipedia page for the first 5 lines '''
        self.assertEqual(
            self.retrieve_first_n_lines(5), self.test_cfg["content_val"]
        )

    def test_return_type_str(self):
        ''' Checks return type of 'get_clean_text' function '''
        self.assertIsInstance(self.processed_text, str)

    def test_get_clean_text(self):
        ''' Checks the cleaned output of 'get_clean_text' function '''
        self.assertEqual(
            self.wiki.get_clean_text(self.test_cfg["get_clean_text_input"]), 
            self.test_cfg["get_clean_text_output"]
        )

    def test_wiki_page_exception(self):
        ''' Checks the wikipedia page exception '''
        self.assertRaises(
            wikipedia.exceptions.WikipediaException, wiki_main, self.incorrect_flag, self.incorrect_topics, self.data_path
        )

if __name__ == "__main__":
    unittest.main()