# Google Cloud Connector

This connector extracts data from Google Cloud storage blobs and then can optinoally store it in a cnvrg dataset. It works identically to s3-connector and only places the files in the output artifacts without any change

## Input
- `bucket_name`: name of the bucket in the google storage blob.
    **Default Value -** 'gildesh_192'
- `folder_names`: names of the folders that contain the data Separated by comma.
    **Default Value -** - 'pose, churn'
- `cnvrg_dataset_name`: name of the cnvrg dataset where you want to store your data
    **Default Value -** - 'testing'

## Code Flow
- The folders are created in the /cnvrg location
- The data is downloaded to the artifacts and then copied to the cnvrg dataset

## Output
-   directory_test/files
-   directory_train/files

## How to run
```
python3 google_cloud_connector.py --bucket gildesh_192 --folder_names --pose, churn --cnvrg_dataset_name testing
```
## References
[Google Cloud Connection to Python](https://towardsdatascience.com/exporting-data-from-google-cloud-platform-72cbe69de695)
[Google Cloud Storage Link](https://console.cloud.google.com/storage/browser/)
