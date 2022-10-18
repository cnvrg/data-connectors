import unittest
import _csv
from monday_connector import boards_and_workspaces, boards, specificquery

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

        # Calling boards and workspaces - retrieve board ids 
        self.board_ids = boards_and_workspaces(self.api_url, self.headers)

    '''
    Globally defined vairables in the script - apiUrl and headers - prevents successful unittesting 
    boards_and_workspaces violates the single responsibilty principle - doing multiple things 
    Re-factored the code to include arguments and reduce the dependency on global variables
    '''
    def test_list_output(self):
        self.assertTrue(self.board_ids, list)

    # Check csv output for boards function 
    def test_csv_output(self):
        self.assertTrue(str(type(boards(self.board_ids, self.api_url, self.headers, self.sep_cols, self.equiv_cols, self.not_flat))), "_csv.reader")

    # Test exception for 'specificquery' function - passing invalid query
    def test_monday_connection_exception(self):
        self.assertRaises(
            Exception, specificquery, self.invalid_query
        )

    # WIP - test specific query json output generation and write a unit-testcase for it