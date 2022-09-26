# Parameters

- `--token` - string, required. API access token for your InfluxDB workspace. For security reasons, we recommend creating/updating the Cnvrg Secret `INFLUXDB_TOKEN` under Project->Settings->Secrets to store the InfluxDB API token. Enter the value ‘Secret’ if the Cnvrg Secret has been created/updated; otherwise enter the actual API token.
- `--url` - string, required. Client url for your InfluxDB workspace. For security reasons, we recommend creating/updating the Cnvrg Secret `INFLUXDB_URL` under Project->Settings->Secrets to store the InfluxDB Client ID. Enter the value ‘Secret’ if the Cnvrg Secret has been created/updated; otherwise enter the actual Client ID.
- `--org` - string, required. Organization email for your InfluxDB workspace. For security reasons, we recommend creating/updating the Cnvrg Secret `INFLUXDB_ORG` under Project->Settings->Secrets to store the InfluxDB Client ID. Enter the value ‘Secret’ if the Cnvrg Secret has been created/updated; otherwise enter the actual Client ID.
- `--bucket` - string, required. Data bucket to pull data from. This can also be stored as Cnvrg Secret `INFLUXDB_BUCKET` under Project->Settings->Secrets to store the InfluxDB Client ID. Enter the value ‘Secret’ if the Cnvrg Secret has been created/updated; otherwise enter the actual Client ID.
- `--range_start` - string, optional. Fetch from starting date in the format of 2020-01-01T00:00:00Z, or specify -1d, -1h, -1m for last day, hour, or minute. For detailed query language, refer to [Influxdb Doc](https://docs.influxdata.com/influxdb/cloud/query-data/flux/Default) value - '2020-01-01T00:00:00Z'
- `--cnvrg_dataset` - string, optional. Name of the cnvrg dataset to store the csv file. Default value - ‘None’
<<<<<<< .merge_file_8q8hqp
- `--file_name` - string, optional. Name of the csv file to be generated. Default value - influxdb.csv’
