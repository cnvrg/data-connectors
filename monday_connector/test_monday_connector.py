import unittest
import json
import os, sys, shutil
import _csv
import yaml
from yaml.loader import SafeLoader
from monday_connector import boards_and_workspaces, boards, specificquery
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
YAML_ARG_TO_TEST = "test_arguments"

class test_monday_connector(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        # Parse the monday connector arguments 
        cfg_path = os.path.dirname(os.path.abspath(__file__))
        cfg_file = cfg_path + "/" + "test_config.yaml"
        self.test_cfg = {}
        with open(cfg_file) as c_info_file:
            self.test_cfg = yaml.load(c_info_file, Loader=SafeLoader)
        self.test_cfg = self.test_cfg[YAML_ARG_TO_TEST]

        # Internal parameters for functions 
        self.headers = {"Authorization": self.test_cfg["api_key"]}
        self.sep_cols = ''
        self.equiv_cols = ''
        self.not_flat = ''

        # Make a Unit-testing data directory
        self.unittest_dir = "unit_test_data"
        self.local_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_path = os.path.join(self.local_dir, self.unittest_dir)
        os.mkdir(self.data_path)

        # Calling boards and workspaces - retrieve board ids 
        self.board_ids = boards_and_workspaces(self.test_cfg["api_url"], self.headers, self.data_path)

    # Skip or comment this out if you need to have a look at the data 
    @classmethod
    def tearDownClass(self):
        shutil.rmtree(self.data_path)

    # Check the list object
    def test_list_output(self):
        self.assertTrue(self.board_ids, list)

    # Check csv output for boards function 
    def test_csv_output(self):
        self.assertTrue(str(type(boards([self.board_ids[0]], self.test_cfg["api_url"], self.headers, self.sep_cols, self.equiv_cols, self.not_flat, self.data_path))), "_csv.reader")

    # Test exception for 'specificquery' function - passing invalid query
    def test_monday_connection_exception(self):
        self.assertRaises(
            Exception, specificquery, self.test_cfg["invalid_query"], self.test_cfg["api_url"], self.test_cfg["api_key"], self.data_path
        )

    # Test Json output 'specific.json' and see if it loads properly 
    def test_JSON_output(self):
        specificquery(self.test_cfg["specific_query"], self.test_cfg["api_url"], self.headers, self.data_path)
        with open(self.data_path + "/" + "specific.json", 'r') as f:
            json_data = json.load(f)
        f.close()
        self.assertTrue(json_data)