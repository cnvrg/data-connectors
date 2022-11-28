# Azure Connector
## _cnvrg_

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

This library allows you to get data from an Azure connector and store it as Cnvrg Dataset which can be later used with other blueprints.
The user needs to provide the container name and the connection string. This library will download all the blobs in the given container and
store them as as cnvrg dataset. The dataset name will be of the format "container_{Year}-{Month}-{Day}_{Hours}-{Minutes}-{Seconds}". The time will be based on the time of run of this library. Example dataset name is, *container_2022-11-18_04-20-58*

## Input
`--container_name` : The name of the container from which all blobs will be downloaded.

`--conn_string` :  The connection string to authenticate your account. The connection string to your storage account can be found in the Azure    Portal under the "Access Keys" section or by running the following CLI command:

```
az storage account show-connection-string -g MyResourceGroup -n MyStorageAccount
```
Connection string looks something like this:
**DefaultEndpointsProtocol=https;AccountName=xxxx;AccountKey=xxxx;EndpointSuffix=core.windows.net**

**Note:** You can provide connection string as input argument or you can set this as an environment variable in your project:

*CONN_STRING* : Your connection string.

Environment key string will override the argument string.

`--account_url` : In case anonymous read access is set at the container level, you can provide account url instead of connection string. This will download the container files without needing any credentials.
An account url will look something like this:
**https://*mystorageaccount*.blob.core.windows.net/**