import os
import argparse
import pandas as pd
from collections import defaultdict
from cnvrgv2 import Cnvrg
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

cnvrg_workdir = os.environ.get("CNVRG_WORKDIR", "/cnvrg")

# writing data to influxdb api
'''
write_api = client.write_api(write_options=SYNCHRONOUS)
for value in range(5):
  point = (
    Point("measurement1")
    .tag("tagname1", "tagvalue1")
    .field("field1", value)
  )
  write_api.write(bucket=bucket, org="kris.pan@cnvrg.io", record=point)
  time.sleep(1) # separate points by 1 second
'''


def parse_parameters():
    """Command line parser."""
    parser = argparse.ArgumentParser(description="""influxdb Connector""")
    parser.add_argument('--token', action='store', dest='token', required=True, 
                            help="""--- influxdb API Access Token ---""")
    parser.add_argument('--url', action='store', dest='url', required=True,
                            help="""--- influxdb access url ---""")
    parser.add_argument('--org', action='store', dest='org', required=True,
                        help="""--- influxdb access organization account ---""")
    parser.add_argument('--bucket', action='store', dest='bucket', required=True,
                        help="""--- bucket where the data is pulled from ---""")
    parser.add_argument('--range_start', action='store', dest='range_start', required=False, default='2020-01-01T00:00:00Z', 
                            help="""--- fetch from starting date in the format of 2020-01-01T00:00:00Z, or specify -1d, -1h, -1m for last day, hour, or minute ---""")
    parser.add_argument('--local_dir', action='store', dest='local_dir', required=False, default=cnvrg_workdir, 
                            help="""--- The path to save the dataset file to ---""")
    parser.add_argument('--cnvrg_dataset', action='store', dest='cnvrg_dataset', required=False, default='None',
                            help="""--- the name of the cnvrg dataset to store in ---""")
    parser.add_argument('--file_name', action='store', dest='file_name', required=False, default='influxdb.csv', 
                            help="""--- name of the dataset csv file ---""")
    return parser.parse_args()



def main():
    args = parse_parameters()
    if args.token.lower() == 'secret':
        args.token = os.environ.get('INFLUXDB_TOKEN')
    if args.url.lower() == 'secret':
        args.url = os.environ.get('INFLUXDB_URL')
    if args.org.lower() == 'secret':
        args.url = os.environ.get('INFLUXDB_ORG')
    if args.bucket.lower() == 'secret':
        args.url = os.environ.get('INFLUXDB_BUCKET')

    client = influxdb_client.InfluxDBClient(url=args.url, token=args.token, org=args.org)
    query_api = client.query_api()

    query = 'from(bucket: "' + args.bucket + '")\n |> range(start:' + args.range_start + ')'
    tables = query_api.query(query, org=args.org)
    table_map = defaultdict(list)

    for table in tables:
        for record in table.records:
            table_map['time'].append(record['_time'])
            table_map['measurement'].append(record['_measurement'])
            table_map['value'].append(record['tagname1'])
    df = pd.DataFrame(table_map)
    df.dropna(inplace=True)
    df.to_csv(args.local_dir+'/'+args.file_name, index=False)

    # Store influxdb csv as cnvrg dataset
    if args.cnvrg_dataset.lower() != 'none':
        cnvrg = Cnvrg()
        ds = cnvrg.datasets.get(args.cnvrg_dataset)
        try:
            ds.reload()
        except:
            print("The provided Dataset was not found")
            print(f"Creating a new dataset named {args.cnvrg_dataset}")
            ds = cnvrg.datasets.create(name=args.cnvrg_dataset)
        print("Uploading files to Cnvrg dataset")
        os.chdir(args.local_dir)
        ds.put_files(paths=[args.file_name])


if __name__ == '__main__':
    main()

