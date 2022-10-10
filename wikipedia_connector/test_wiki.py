import unittest
import os
from wiki import WikiPage
from bs4 import BeautifulSoup
import urllib.request
from urllib.request import urlopen

class TestWiki(unittest.TestCase):
    @classmethod
    def setUpClass(self) -> None:
        self.args = []
        with open("arguments.txt") as f:
            self.args.append(f.readline())
        self.wiki = WikiPage(str(self.args[0]))

        # Extracting raw text - for 'get_clean_text' argument
        soup = BeautifulSoup(
            urlopen("https://en.wikipedia.org/wiki/" + str(self.args[0])).read(), "lxml"
        )
        self.raw_text = ""
        for paragraph in soup.find_all("p"):
            self.raw_text += paragraph.text

        # Setup for testing 'get_wiki_page' and 'get_clean_text' functions
        self.wiki_output = self.wiki.get_wiki_page(str(self.args[0]))
        self.processed_text = self.wiki.get_clean_text(self.raw_text)

        # Validate 'get_wiki_page' content
        with open("wiki_output.txt") as f:
            self.content_val = f.read()
        self.content_val = ' ' + self.content_val + ' '

    def test_return_type_list(self):
        # Checks if the 'get_wiki_page' function returns list
        self.assertIsInstance(self.wiki_output, list)

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
        # Checks the content validity
        self.assertEquals(
            self.wiki_output[0], self.content_val
        )

    def test_return_type_str(self):
        # Checks if the 'get_clean_text' function returns string
        self.assertIsInstance(self.processed_text, str)

    # WIP - Develop a test-case to check 'get_clean_text' functionality

if __name__ == "__main__":
    unittest.main()