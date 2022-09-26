import pandas as pd
import unittest
import os
import argparse
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_connector import influxdb_query, custom_bucket_formatting


class TestInfluxdb(unittest.TestCase):
    def setUp(self) -> None:
        self.args = []
        # read text file containing required arguments on each line
        with open("arguments.txt") as f:
            self.args.append(f.readline())


class TestInfluxdbQuery(TestInfluxdb):
    def test_return_type(self):
        """Checks if the function returns dictionary"""
        self.assertIsInstance(
            influxdb_query(
                self.args[0], self.args[1], self.args[2], self.args[3], self.args[4]
            ),
            dict,
        )


class TestCustomBucketFormatting(TestInfluxdb):
    def __init__(self):
        self.csv_builder = influxdb_query(
            self.args[0], self.args[1], self.args[2], self.args[3], self.args[4]
        )

    def test_return_type(self):
        """Checks if the function returns dictionary"""
        self.assertIsInstance(
            custom_bucket_formatting(self.csv_builder, self.args[3]), dict
        )
