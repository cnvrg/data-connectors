import os
import argparse
import pandas as pd
from collections import defaultdict
from cnvrgv2 import Cnvrg
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

cnvrg_workdir = os.environ.get("CNVRG_WORKDIR", "/cnvrg")


def parse_parameters():
    """Command line parser."""
    parser = argparse.ArgumentParser(description="""influxdb Connector""")
    parser.add_argument(
        "--token",
        action="store",
        dest="token",
        required=True,
        help="""--- influxdb API Access Token ---""",
    )
    parser.add_argument(
        "--url",
        action="store",
        dest="url",
        required=True,
        help="""--- influxdb access url ---""",
    )
    parser.add_argument(
        "--org",
        action="store",
        dest="org",
        required=True,
        help="""--- influxdb access organization account ---""",
    )
    parser.add_argument(
        "--bucket",
        action="store",
        dest="bucket",
        required=True,
        help="""--- bucket where the data is pulled from ---""",
    )
    parser.add_argument(
        "--range_start",
        action="store",
        dest="range_start",
        required=False,
        default="-10y",
        help="""--- fetch from starting date in the format of 2020-01-01T00:00:00Z, or specify -1d, -1h, -1m for last day, hour, or minute ---""",
    )
    parser.add_argument(
        "--local_dir",
        action="store",
        dest="local_dir",
        required=False,
        default=cnvrg_workdir,
        help="""--- The path to save the dataset file to ---""",
    )
    parser.add_argument(
        "--cnvrg_dataset",
        action="store",
        dest="cnvrg_dataset",
        required=False,
        default="None",
        help="""--- the name of the cnvrg dataset to store in ---""",
    )
    parser.add_argument(
        "--file_name",
        action="store",
        dest="file_name",
        required=False,
        default="influxdb.csv",
        help="""--- name of the dataset csv file ---""",
    )
    return parser.parse_args()

class NoneCnvrgDatasetError(Exception):
    """Raise if message is None object"""
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "NoneMessageError: Please ensure the input is valid!"

def influxdb_query(url, token, org, bucket, range_start):
    """
    Creates dictionary from query of given inputs
        Args:
            url: https address of influxdb cloud
            token: token for accessing influxdb cloud
            org: email address for user authentication
            bucket: name of the bucket to access
            range_start: starting range for query, default set to last 10 years of data
    Returns:
        A dictionary containing time and field columns from influxdb query
    """
    client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
    query_api = client.query_api()
    if range_start.lower() != "none":
        query = 'from(bucket: "' + bucket + '")\n |> range(start:' + range_start + ")"
    else:
        query = 'from(bucket: "' + bucket + '")\n |> range(start:-10y)'
    tables = query_api.query(query, org=org)
    csv_builder = dict()
    csv_builder["time"] = []

    # build dictionary from query
    for table in tables:
        for record in table.records:
            # scrape all fields from query results
            if record["_field"] not in csv_builder:
                csv_builder[record["_field"]] = []
            csv_builder[record["_field"]].append(record["_value"])
            csv_builder["time"].append(record["_time"])
    # since time is shown for every field, remove redundancy in time
    time_len = len(csv_builder["time"]) // (len(csv_builder) - 1)
    csv_builder["time"] = csv_builder["time"][:time_len]
    
    # truncate datetime string so that the +00:00 is removed 
    sliced_time = []
    for t in csv_builder["time"]:
        sliced_time.append(str(t)[:19])
    csv_builder["time"] = sliced_time

    return csv_builder

def main():
    args = parse_parameters()
    if args.token.lower() == "secret":
        args.token = os.environ.get("INFLUXDB_TOKEN")
    if args.url.lower() == "secret":
        args.url = os.environ.get("INFLUXDB_URL")
    if args.org.lower() == "secret":
        args.org = os.environ.get("INFLUXDB_ORG")
    if args.bucket.lower() == "secret":
        args.bucket = os.environ.get("INFLUXDB_BUCKET")
    # return dictionary from custom query
    csv_builder = influxdb_query(
        args.url, args.token, args.org, args.bucket, args.range_start
    )

    # build pandas dataframe for csv
    df = pd.DataFrame(csv_builder)
    df.to_csv(args.local_dir + "/" + args.file_name, index=False)

    # Store influxdb csv as cnvrg dataset
    if args.cnvrg_dataset.lower() == "none":
        raise NoneCnvrgDatasetError()
    else:    
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


if __name__ == "__main__":
    main()
