import unittest

# import os
from wiki import WikiPage

from bs4 import BeautifulSoup
# import urllib.request
from urllib.request import urlopen


class demoCalss(unittest.TestCase):
    def test_hellowold(self):
        print("hello world")
        self.assertFalse(False)


class TestWiki(unittest.TestCase):
    @classmethod
    def setUpClass(self) -> None:
        self.args = []
        with open("arguments.txt") as f:
            self.args.append(f.readline())
        self.wiki = WikiPage(str(self.args[0]))

        soup = BeautifulSoup(
            urlopen("https://en.wikipedia.org/wiki/" + str(self.args[0])).read(), "lxml"
        )
        self.text = ""
        for paragraph in soup.find_all("p"):
            self.text += paragraph.text

    # class TestGetWikiPage(TestWiki):
    def test_return_type_list(self):
        # Checks if the function returns list
        print("running first ")
        self.assertIsInstance(self.wiki.get_wiki_page(str(self.args[0])), list)

    # class TestGetCleanText(TestWiki):
    def test_return_type_str(self):
        print("running second ")
        #Checks if the function returns string
        self.assertIsInstance(self.wiki.get_clean_text(self.text), str)


if __name__ == "__main__":
    unittest.main()
