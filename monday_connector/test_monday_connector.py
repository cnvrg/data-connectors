import unittest
import json
import os, sys, shutil
import _csv
from monday_connector import boards_and_workspaces, boards, specificquery
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class test_monday_connector(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        # Parse the monday connector arguments 
        self.args = []
        with open("arguments.txt") as f:
            for line in f:
                self.args.append(line[:-1])

        # Store account credentails 
        self.api_url = "https://api.monday.com/v2"
        self.api_key = self.args[0]
        self.headers = {"Authorization": self.api_key}
        self.specific_query = self.args[1]
        self.invalid_query = ''
        self.sep_cols = ''
        self.equiv_cols = ''
        self.not_flat = ''
        self.unittest_dir = "unit_test_data"
        self.local_dir = os.path.dirname(os.path.abspath(__file__))
        # Make a Unit-testing data directory
        self.data_path = os.path.join(self.local_dir, self.unittest_dir)
        os.mkdir(self.data_path)

        # Calling boards and workspaces - retrieve board ids 
        self.board_ids = boards_and_workspaces(self.api_url, self.headers, self.data_path)

    # Skip or comment this out if you need to have a look at the data 
    @classmethod
    def tearDownClass(self):
        shutil.rmtree(self.data_path)

    '''
    Globally defined vairables in the script - apiUrl and headers - prevents successful unittesting 
    boards_and_workspaces violates the single responsibilty principle - doing multiple things 
    Re-factored the code to include arguments and reduce the dependency on global variables
    '''
    def test_list_output(self):
        self.assertTrue(self.board_ids, list)

    # Check csv output for boards function 
    def test_csv_output(self):
        self.assertTrue(str(type(boards([self.board_ids[0]], self.api_url, self.headers, self.sep_cols, self.equiv_cols, self.not_flat, self.data_path))), "_csv.reader")

    # Test exception for 'specificquery' function - passing invalid query
    def test_monday_connection_exception(self):
        self.assertRaises(
            Exception, specificquery, self.invalid_query, self.api_url, self.api_key, self.data_path
        )

    # Test Json output 'specific.json' and see if it loads properly 
    def test_JSON_output(self):
        specificquery(self.specific_query, self.api_url, self.headers, self.data_path)
        with open(self.data_path + "/" + "specific.json", 'r') as f:
            json_data = json.load(f)
        f.close()
        self.assertTrue(json_data)
