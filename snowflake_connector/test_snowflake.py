import unittest
import os
import sys
import pandas
from snowflake_connector import connect, to_csv, run, close_connection, to_df

class TestSnowflake(unittest.TestCase):
    def setUp(self) -> None:
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

class TestSnowFlakeConnection(TestSnowflake):
    def test_connection_status(self):
        self.assertIsNotNone(
            connect(self.password, self.warehouse, self.account, self.user, self.database, self.schema)
        )

    def test_connection_execption(self):
        self.assertRaises(
            SystemExit, connect, self.incorrect_password, self.warehouse, self.account, self.user, self.database, self.schema
        )

    def test_close_connection_exception(self):
        self.assertRaises(
            SystemExit, close_connection, None
        )

class TestRunQuery(TestSnowflake):
    def test_run_query(self):
        self.snowflake_connection = connect(self.password, self.warehouse, self.account, self.user, self.database, self.schema)
        self.assertIsNotNone(
            run(self.snowflake_connection, self.query)
        )

    def test_run_execption(self):
        self.snowflake_connection = connect(self.password, self.warehouse, self.account, self.user, self.database, self.schema)
        self.assertRaises(
            SystemExit, run, self.snowflake_connection, None
        )

class TestDataFrameOutput(TestSnowflake):
    def test_df_output(self):
        self.snowflake_connection = connect(self.password, self.warehouse, self.account, self.user, self.database, self.schema)
        self.assertIsInstance(
            to_df(self.snowflake_connection, self.query), pandas.core.frame.DataFrame
        )

# Skip this unit-test if the '/cnvrg/' path is set in the script 
class TestCsvOutput(TestSnowflake):
    def test_csv_output(self):
        self.snowflake_connection = connect(self.password, self.warehouse, self.account, self.user, self.database, self.schema)
        self.assertTrue(str(type(to_csv(self.snowflake_connection, self.query, self.output_file))), "_csv.reader")

if __name__ == '__main__':
    unittest.main()