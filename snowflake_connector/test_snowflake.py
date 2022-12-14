import shutil
import unittest
import os
import sys
import pandas
import yaml
from yaml.loader import SafeLoader
import numpy
from snowflake_connector import connect, to_csv, run, close_connection, to_df
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
YAML_ARG_TO_TEST = "test_arguments"

class test_snowflake_connector(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        # Parse the snowflake parameters
        cfg_path = os.path.dirname(os.path.abspath(__file__))
        cfg_file = cfg_path + "/" + "test_config.yaml"
        self.test_cfg = {}
        with open(cfg_file) as c_info_file:
            self.test_cfg = yaml.load(c_info_file, Loader=SafeLoader)
        self.test_cfg = self.test_cfg[YAML_ARG_TO_TEST]

        # Make a Unit-testing data directory    
        self.unittest_dir = "unit_test_data"
        self.local_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_path = os.path.join(self.local_dir, self.unittest_dir)
        os.mkdir(self.data_path)

        # Intialize connection for 'query' testing
        self.snowflake_connection = connect(
            self.test_cfg["password"], 
            self.test_cfg["warehouse"], 
            self.test_cfg["account"], 
            self.test_cfg["user"], 
            self.test_cfg["database"], 
            self.test_cfg["schema"]
            )

        '''
        Create a file for comparison - this file is uploaded on snowflake for comparison
           TEST_COLUMN_1  TEST_COLUMN_2
                       1              2
                       2              3
                       3              4
                       4              5
                       5              6
        '''
        self.compare_data = {"TEST_COLUMN_1": [1, 2, 3, 4, 5], "TEST_COLUMN_2": [2, 3, 4, 5, 6]}
        self.df = pandas.DataFrame(self.compare_data)

        # Create a csv file and compare it's content
        self.pulled_csv_output = to_csv(self.data_path, self.snowflake_connection, self.test_cfg["query"], self.test_cfg["output_file"])
        self.pulled_df = pandas.read_csv(self.data_path + "/" + self.test_cfg["output_file"])

    @classmethod
    def tearDownClass(self):
        close_connection(self.snowflake_connection)
        shutil.rmtree(self.data_path)

    # Test snowflake connection success
    def test_connection(self):
        self.assertTrue(self.snowflake_connection)

    # Test snowflake connection exception
    def test_connection_exception(self):
        self.assertRaises(
            SystemExit, connect, 
            self.test_cfg["incorrect_password"], 
            self.test_cfg["warehouse"], 
            self.test_cfg["account"], 
            self.test_cfg["user"], 
            self.test_cfg["database"], 
            self.test_cfg["schema"]
        )

    # Test snowflake close connection exception
    def test_close_exception(self):
        self.assertRaises(
            SystemExit, close_connection, None
        )

    # Test snowflake run query 
    def test_run_query(self):
        self.assertTrue(
            run(self.snowflake_connection, self.test_cfg["query"])
        )

    # Test snowflake run query exception
    def test_run_query_exception(self):
        self.assertRaises(
            SystemExit, run, self.snowflake_connection, None
        )

    # Test data-frame output 
    def test_df_output(self):
        self.assertIsInstance(
            to_df(self.snowflake_connection, self.test_cfg["query"]), pandas.core.frame.DataFrame
        )

    # Test csv output 
    def test_csv_output(self):
        self.assertTrue(str(type(self.pulled_csv_output)), "_csv.reader")

    # Test the content of the data frames - compare
    def df_equals(self):
        return (self.df.values == self.pulled_df.values).all()

    # Test the csv content of both the files
    def test_csv_content(self):
        self.assertTrue(
            self.df_equals()
        )

if __name__ == '__main__':
    unittest.main()