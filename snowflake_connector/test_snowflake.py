import unittest
import os
import sys
from snowflake_connector import connect

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

if __name__ == '__main__':
    unittest.main()
