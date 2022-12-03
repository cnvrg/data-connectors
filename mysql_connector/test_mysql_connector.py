import unittest
import os
import yaml
import pandas as pd
import mysql.connector
import yaml
from yaml.loader import SafeLoader
from pydoc import locate
from mysql_connector import (
    table_creation_unfiltered,
    table_creation_filtered
)
YAML_ARG_TO_TEST = "test_arguments"
YAML_ARG_TO_COMP = "results_arguments"

class Test_mysql_connector(unittest.TestCase):
    @classmethod
    def setUpClass(self) -> None:
        # Parse the wiki page
        cfg_path = os.path.dirname(os.path.abspath(__file__))
        cfg_file = cfg_path + "/" + "test_config.yaml"
        cfg_file1 = cfg_path + "/" + "test_config1.yaml"
        cfg_file2 = cfg_path + "/" + "test_config2.yaml"
        cfg_file3 = cfg_path + "/" + "test_config3.yaml"
        cfg_file4 = cfg_path + "/" + "test_config4.yaml"
        result_file = cfg_path + "/" + "results_config.yaml"
        result_file1 = cfg_path + "/" + "results_config1.yaml"
        result_file2 = cfg_path + "/" + "results_config2.yaml"
        result_file3 = cfg_path + "/" + "results_config3.yaml"
        result_file4 = cfg_path + "/" + "results_config4.yaml"

        self.test_cfg = {}
        self.test_cfg1 = {}
        self.test_cfg2 = {}
        self.test_cfg3 = {}
        self.test_cfg4 = {}
        self.results_cfg = {}
        self.results_cfg1 = {}
        self.results_cfg2 = {}
        self.results_cfg3 = {}
        self.results_cfg4 = {}

        with open(cfg_file) as c_info_file:
            self.test_cfg = yaml.load(c_info_file, Loader=SafeLoader)
        with open(cfg_file1) as c_info_file:
            self.test_cfg1 = yaml.load(c_info_file, Loader=SafeLoader)
        with open(cfg_file2) as c_info_file:
            self.test_cfg2 = yaml.load(c_info_file, Loader=SafeLoader)
        with open(cfg_file3) as c_info_file:
            self.test_cfg3 = yaml.load(c_info_file, Loader=SafeLoader)
        with open(cfg_file4) as c_info_file:
            self.test_cfg4 = yaml.load(c_info_file, Loader=SafeLoader)

        with open(result_file) as c_res_file:
            self.results_cfg = yaml.load(c_res_file, Loader=SafeLoader)
        with open(result_file1) as c_res_file:
            self.results_cfg1 = yaml.load(c_res_file, Loader=SafeLoader)
        with open(result_file2) as c_res_file:
            self.results_cfg2 = yaml.load(c_res_file, Loader=SafeLoader)
        with open(result_file3) as c_res_file:
            self.results_cfg3 = yaml.load(c_res_file, Loader=SafeLoader)
        with open(result_file4) as c_res_file:
            self.results_cfg4 = yaml.load(c_res_file, Loader=SafeLoader)

        self.test_cfg = self.test_cfg[YAML_ARG_TO_TEST]
        self.test_cfg1 = self.test_cfg1[YAML_ARG_TO_TEST]
        self.test_cfg2 = self.test_cfg2[YAML_ARG_TO_TEST]
        self.test_cfg3 = self.test_cfg3[YAML_ARG_TO_TEST]
        self.test_cfg4 = self.test_cfg4[YAML_ARG_TO_TEST]
        
        self.results_cfg = self.results_cfg[YAML_ARG_TO_COMP]
        self.results_cfg1 = self.results_cfg1[YAML_ARG_TO_COMP]
        self.results_cfg2 = self.results_cfg2[YAML_ARG_TO_COMP]
        self.results_cfg3 = self.results_cfg3[YAML_ARG_TO_COMP]
        self.results_cfg4 = self.results_cfg4[YAML_ARG_TO_COMP]
        
        host = 'sql9.freemysqlhosting.net' #self.test_cfg['host']
        user = 'sql9578677' #self.test_cfg['user']
        pwd = 'Xz5NyxtDql' #self.test_cfg['pwd']
        database = 'sql9578677' #self.test_cfg['database']
        database = database.split(',')
        mydb = mysql.connector.connect(
            host=host,
            user=user,
            password=pwd,
            database=database
        )
        cursor = mydb.cursor(buffered=True)
        ############ Testing Filtered DataFrame of Employees#######
        tables = self.test_cfg['tables_views']
        columns_to_filter = self.test_cfg['columns_to_filter']
        tables_columns_filters = self.test_cfg['tables_columns_filters']
        tables_views_columns = self.test_cfg['tables_views_columns']
        i = int(self.test_cfg['i'])
        j = int(self.test_cfg['j'])
        tables_split = tables.split(',')
        filter_col_names_table = columns_to_filter.split('!')[0]
        pre_table_filters = tables_columns_filters.split('|')
        table_columns = tables_views_columns.split('!')[0]
        individual_table_cols = table_columns.split('|')
        self.type_case0 = table_creation_filtered(database, tables_split, pre_table_filters, j, individual_table_cols, i, filter_col_names_table, cursor, mydb)[0]
        self.row_case0 = table_creation_filtered(database, tables_split, pre_table_filters, j, individual_table_cols, i, filter_col_names_table, cursor, mydb)[0].shape[0]
        self.col_case0 = table_creation_filtered(database, tables_split, pre_table_filters, j, individual_table_cols, i, filter_col_names_table, cursor, mydb)[0].shape[1]
        ############ Testing UnFiltered DataFrame of Mentors#######
        tables = self.test_cfg1['tables_views']
        tables_split = tables.split(',')
        columns_to_filter = self.test_cfg1['tables_columns_filters']
        type_object = locate(self.results_cfg1['type'])
        i = int(self.test_cfg1['i'])
        j = int(self.test_cfg1['j'])
        filter_col_names_table = columns_to_filter.split('!')[0]
        self.type_case1 = table_creation_unfiltered(database, host, user, pwd, tables_split, filter_col_names_table, j, i,cursor,mydb)[0]
        self.row_case1 = table_creation_unfiltered(database, host, user, pwd, tables_split, filter_col_names_table, j, i,cursor,mydb)[0].shape[0]
        self.col_case1 = table_creation_unfiltered(database, host, user, pwd, tables_split, filter_col_names_table, j, i,cursor,mydb)[0].shape[1]
        ############ Testing Custom Function#######
        custom_query = self.test_cfg4['custom_query']
        self.type_case4 = custom_function(custom_query, database, i, host, user, password)
        self.row_case4 = custom_function(custom_query, database, i, host, user, password).shape[0]
        self.col_case4 = custom_function(custom_query, database, i, host, user, password).shape[1]

    def test_first(self):
        type_object = locate(self.results_cfg['type'])
        rows_left = int(self.results_cfg['rows_df'])
        cols_left = int(self.results_cfg['cols_df'])
        self.assertEqual(rows_left,self.row_case0)
        self.assertEqual(rows_left,self.col_case0)
        self.assertIsInstance(type_object, self.type_case0)        
        cursor.close()

    def test_second(self):
        type_object = locate(self.results_cfg1['type'])
        rows_left = int(self.results_cfg1['rows_df'])
        cols_left = int(self.results_cfg1['cols_df'])
        self.assertEqual(rows_left,self.row_case1)
        self.assertEqual(rows_left,self.col_case1)
        self.assertIsInstance(type_object,self.type_case1)        
        cursor.close()

    def test_third(self):
        type_object = locate(self.results_cfg4['type'])
        rows_left = int(self.results_cfg4['rows_df'])
        cols_left = int(self.results_cfg4['cols_df'])
        self.assertEqual(rows_left,self.row_case4)
        self.assertEqual(rows_left,self.col_case4)
        self.assertIsInstance(type_object, self.type_case4)        
        cursor.close()


if __name__ == '__main__':
    unittest.main()