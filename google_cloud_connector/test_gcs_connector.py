import unittest
import os
import yaml
import pathlib
import pandas as pd
from google.cloud import storage
from yaml.loader import SafeLoader
from pydoc import locate
from gcs import (
    Download_Bucket
)
YAML_ARG_TO_TEST = "test_arguments"
YAML_ARG_TO_COMP = "results_arguments"

class Test_gcs_connector(unittest.TestCase):
    @classmethod
    def setUpClass(self) -> None:
        # Parse the wiki page
        cfg_path = os.path.dirname(os.path.abspath(__file__))
        cfg_file = cfg_path + "/" + "test_config.yaml"
        cfg_file1 = cfg_path + "/" + "test_config1.yaml"
        result_file = cfg_path + "/" + "results_config.yaml"
        result_file1 = cfg_path + "/" + "results_config1.yaml"

        self.test_cfg = {}
        self.test_cfg1 = {}
        self.results_cfg = {}
        self.results_cfg1 = {}

        with open(cfg_file) as c_info_file:
            self.test_cfg = yaml.load(c_info_file, Loader=SafeLoader)
        with open(cfg_file1) as c_info_file:
            self.test_cfg1 = yaml.load(c_info_file, Loader=SafeLoader)

        with open(result_file) as c_res_file:
            self.results_cfg = yaml.load(c_res_file, Loader=SafeLoader)
        with open(result_file1) as c_res_file:
            self.results_cfg1 = yaml.load(c_res_file, Loader=SafeLoader)

        self.test_cfg = self.test_cfg[YAML_ARG_TO_TEST]
        self.test_cfg1 = self.test_cfg1[YAML_ARG_TO_TEST]
        
        self.results_cfg = self.results_cfg[YAML_ARG_TO_COMP]
        self.results_cfg1 = self.results_cfg1[YAML_ARG_TO_COMP]

        ############ Testing case where we have all folders in the bucket#######
        scripts_dir = pathlib.Path(__file__).parent.resolve()    
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(scripts_dir, 'arctic-idiom-370706-07692fc76fd5.json')
 
    def test_first(self):
        def flatten(iterable):
            cnt = 0
            for i in range(len(iterable)):
                cnt = cnt+len(iterable[i])
            return cnt

        if self.test_cfg['folders'] == 'all':
            folder_list = 'pose,churn'
        else:
            folder_list = self.test_cfg['folders']
        gcp = Download_Bucket(self.test_cfg['bucket'], folder_list)
        listfiles = gcp.file_name_compilation()
        print('First test')
        print(listfiles)
        if len(listfiles) > 1:
            lenlist = flatten(listfiles)
        else:
            lenlist = len(listfiles[0])        

        typeobject = locate(self.results_cfg['type'])
        self.assertEqual(lenlist,int(self.results_cfg['unique_folder_cnt']))
        self.assertEqual(type(listfiles),typeobject)

    def test_second(self):
        def flatten(iterable):
            cnt = 0
            for i in range(len(iterable)):
                cnt = cnt+len(iterable[i])
            return cnt
        
        if self.test_cfg1['folders'] == 'all':
            print('all')
            folder_list = 'pose,churn'
        else:
            folder_list = self.test_cfg1['folders']
        gcp = Download_Bucket(self.test_cfg1['bucket'], folder_list)
        listfiles = gcp.file_name_compilation()
        print('Second test')
        print(listfiles)
        if len(listfiles) > 1:
            lenlist = flatten(listfiles)
        else:
            lenlist = len(listfiles[0])        
        typeobject = locate(self.results_cfg1['type'])
        self.assertEqual(lenlist,int(self.results_cfg1['unique_folder_cnt']))
        self.assertEqual(type(listfiles),typeobject)

if __name__ == '__main__':
    unittest.main()