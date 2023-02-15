import os
from cnvrgv2 import Cnvrg
import shutil
from google.cloud import storage
import argparse
import pathlib
import itertools
def argument_parser():
    parser = argparse.ArgumentParser(description="""Creator""")
    parser.add_argument(
        "--bucket_name",
        action="store",
        dest="bucket_name",
        required=True,
        default="gildesh_192",
        help="""name of the bucket where your data is stored""",
    )
    parser.add_argument(
        "--folder_names",
        action="store",
        dest="folder_names",
        required=True,
        default="pose",
        help="""name of the folder which is to be downloaded""",
    )
    parser.add_argument(
        "--cnvrg_dataset_name",
        action="store",
        dest="cnvrg_dataset_name",
        required=True,
        default="sample",
        help="""name of the dataset where you will store the file""",
    )
    return parser.parse_args()

class Download_Bucket():
  def __init__(self, bucket_name, folder_name):
    self.bucket_name = bucket_name
    self.folder_name = folder_name
    self.client = storage.Client()
    self.bucket = self.client.get_bucket(self.bucket_name)
  def file_name_compilation(self):
    list_of_all_files = []
    if self.folder_name != 'all':
        for self.folder_name in self.folder_name.split(','):
            fold_1 = []
            for blob in self.client.list_blobs(self.bucket_name, prefix=self.folder_name):
                if not str(blob).split(',')[1].endswith('/'):
                    fold_1.append(str(blob).split(',')[1].replace(' ',''))
            list_of_all_files.append(fold_1)
    else:
        fold_1 = []
        for blob in self.client.list_blobs(self.bucket_name):
            if not str(blob).split(',')[1].endswith('/'):
                fold_1.append(str(blob).split(',')[1].replace(' ',''))
        list_of_all_files.append(fold_1)
    return list_of_all_files
        #list_of_all_files.append(':')
  def file_saving(self,list_of_all_files, path):
    for file_list in list_of_all_files:
        print('file')
        print(file_list)
        blob = [self.bucket.blob(file) for file in file_list]
        filename_collection = [os.path.join(path, file) for file in file_list]
        [blob1.download_to_filename(dest_file_name)
         for blob1 in blob for dest_file_name in filename_collection]

def save_to_cnvrg(files_list,storage_name,ds):
    print('Saving to cnvrg running')
    cnvrg = Cnvrg()
    ds_name = storage_name
    print(storage_name)
    print('list of files is below')
    print(files_list)
    ds = cnvrg.datasets.create(name=ds_name)    
    ds.put_files(paths=files_list)

def main():
    args = argument_parser()
    scripts_dir = pathlib.Path(__file__).parent.resolve()
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(scripts_dir, 'arctic-idiom-370706-07692fc76fd5.json')
    for folder_names in args.folder_names.split(','):
        indv_folder_name = os.path.join('/cnvrg',folder_names)
        os.makedirs(indv_folder_name, exist_ok=True)
    gcp = Download_Bucket(args.bucket_name, args.folder_names)
    list_of_all_files = gcp.file_name_compilation()
    path = '/cnvrg'
    gcp.file_saving(list_of_all_files, path)
    cnvrge = Cnvrg()
    if args.cnvrg_dataset_name != 'None':
        print('Cnvrg Dataset Code Running')
        ds = cnvrge.datasets.create(name=args.cnvrg_dataset_name)
        file_string = list(itertools.chain.from_iterable(list_of_all_files))
        file_string = ['/cnvrg/'+x for x in file_string]
        save_to_cnvrg(file_string,args.cnvrg_dataset_name,ds)

if __name__== "__main__":
    main()