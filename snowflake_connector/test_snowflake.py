import unittest
import os
import sys
import pandas
from snowflake_connector import connect, to_csv, run, close_connection, to_df

class test_snowflake_connector(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        # Parse the snowflake parameters
        self.args = []
        with open("arguments.txt") as f:
            for line in f:
                self.args.append(line[:-1])

        # Store the account credentails for further testing
        self.user = self.args[0]
        self.password = self.args[1]
        self.account = self.args[2]
        self.database = self.args[3]
        self.query = self.args[4]
        self.output_file = self.args[5]
        self.warehouse = ''
        self.schema = ''
        self.incorrect_password = 'garbage'

        # Intialize connection for 'query' testing
        self.snowflake_connection = connect(self.password, self.warehouse, self.account, self.user, self.database, self.schema)

    @classmethod
    def tearDownClass(self):
        close_connection(self.snowflake_connection)

    # Test snowflake connection success
    def test_connection(self):
        self.assertTrue(self.snowflake_connection)

    # Test snowflake connection exception
    def test_connection_exception(self):
        self.assertRaises(
            SystemExit, connect, self.incorrect_password, self.warehouse, self.account, self.user, self.database, self.schema
        )

    # Test snowflake close connection exception
    def test_close_exception(self):
        self.assertRaises(
            SystemExit, close_connection, None
        )

    # Test snowflake run query 
    def test_run_query(self):
        self.assertTrue(
            run(self.snowflake_connection, self.query)
        )

    # Test snowflake run query exception
    def test_run_query_exception(self):
        self.assertRaises(
            SystemExit, run, self.snowflake_connection, None
        )

    # Test data-frame output 
    def test_df_output(self):
        self.assertIsInstance(
            to_df(self.snowflake_connection, self.query), pandas.core.frame.DataFrame
        )

    # Test csv output
    def test_csv_output(self):
        self.assertTrue(str(type(to_csv(self.snowflake_connection, self.query, self.output_file))), "_csv.reader")

if __name__ == '__main__':
    unittest.main()