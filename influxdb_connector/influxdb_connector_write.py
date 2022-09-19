import os
import argparse
import pandas as pd
from collections import defaultdict
# from cnvrgv2 import Cnvrg
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

cnvrg_workdir = os.environ.get("CNVRG_WORKDIR", "/cnvrg")
url = "https://us-east-1-1.aws.cloud2.influxdata.com"
org =  "kris.pan@cnvrg.io"
token = "I8idv5QMDs0IbuOU2vnxOljNNGU1bl_dvUYSLxkDFLugeerxB5NqGYHbh0uWSrdEV6g2PjGBGISm_0-n7_OL1A=="
bucket = "anomaly_detection"
# writing data to influxdb api
client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)


# df = pd.read_csv("github/data-connectors/influxdb_connector/influxdb_test_date_filled.csv")
'''
df['time'] = pd.to_datetime(df['time'], errors='ignore')
df['time'] = df['time'].fillna(value=pd.to_datetime('2022-09-01 01:01:01'))
df[['Accelerometer1RMS','Accelerometer2RMS','Current','Pressure','Temperature','Thermocouple','Voltage','Volume Flow RateRMS']] = \
    df[['Accelerometer1RMS','Accelerometer2RMS','Current','Pressure','Temperature','Thermocouple','Voltage','Volume Flow RateRMS']].fillna(value=0.0)
df[['anomaly','changepoint']] = df[['anomaly','changepoint']].fillna(3)
df['status'] = df['status'].fillna('None')
convert_dict = {'anomaly': int,'changepoint': int, 'status': str}
df = df.astype(convert_dict)
print(df.dtypes)
write_api = client.write_api(write_options=SYNCHRONOUS)
'''

# for value in range(5):
#   point = (
#     Point("measurement1")
#     .tag("tagname1", "tagvalue1")
#     .field("field1", value)
#   )
#   write_api.write(bucket=bucket, org="kris.pan@cnvrg.io", record=point)
#   time.sleep(1) # separate points by 1 second

# def read_data():
#     with open("github/data-connectors/influxdb_connector/influxdb_test.csv") as f:
#         return [x.split(',') for x in f.readlines()[1:]]

# data = read_data()
# write_api = client.write_api(write_options=SYNCHRONOUS)
# for metric in data:
#     influx_metric = [{
#         'time': metric[0],
#         'fields': {
#              'Accelerometer1RMS': metric[1],
#              'Accelerometer2RMS': metric[2],
#              'Current': metric[3],
#              'Pressure': metric[4],
#              'Temperature': metric[5],
#              'Thermocouple': metric[6],
#              'Voltage': metric[7],
#              'VolumeFlowRateRMS': metric[8],
#              'anomaly': metric[9],
#              'changepoint': metric[10],
#              'status': metric[11]
#         }
#     }]
# 2015-08-18T00:00:00Z
# 1577836800000000000

# bucket="DailyDelhiClimate"


# linux_time = pd.to_datetime('2022-09-16T05:48:17Z')
# point = (
#     Point('simple') 
#     .time(linux_time) 
#     .field('measurement1',10.05)
# )

# write_api.write(bucket=bucket, org="kris.pan@cnvrg.io", record=point)
# print('data written')

# with InfluxDBClient(url=url, token=token, org=org) as client:
#     client.write_api(write_options=SYNCHRONOUS).write(bucket=bucket, record=df[:1], data_frame_measurement_name="measurement1", data_frame_timestamp_column="time")
#     print('done')
# columns = df.columns
# num_col = len(columns)
query_api = client.query_api()
# TODO validate bucket and range 
query = 'from(bucket: "' + bucket + '")\n |> range(start: -10y)'
tables = query_api.query(query, org=org)
csv_builder = dict()
# for col in columns:
#     csv_builder[col] = []
csv_builder['time'] = []

for table in tables:
    for record in table.records:
        if record['_field'] not in csv_builder:
            csv_builder[record['_field']] = []
        csv_builder[record['_field']].append(record['_value'])
        csv_builder['time'].append(record['_time'])
time_len = len(csv_builder['time']) // (len(csv_builder) - 1)
csv_builder['time'] = csv_builder['time'][:time_len]

# custom formatting for anomaly detection blueprint
sliced_time = []
for t in csv_builder['time']:
    sliced_time.append(str(t)[:19])

csv_builder['anomaly'] = [1 if x == 3 else x for x in csv_builder['anomaly']]
csv_builder['time'] = sliced_time

# print(csv_builder['anomaly'])
# print(csv_builder['time'])

df = pd.DataFrame(csv_builder)
print(df[:5])
# for t in csv_builder['time']:
#     print(str(t)[:19])
# print(len(csv_builder['Current']))
# csv_builder['time'] = csv_builder['time'][:len(csv_builder)-1]
# print(csv_builder['time'], len(csv_builder['time']))
#  tables = query_api.query(query, org=args.org)
#     table_map = defaultdict(list)

#     for table in tables:
#         # TODO parse all columns
#         for record in table.records:
#             for key, value in record.items():
#             # table_map['time'].append(record['_time'])
#             # table_map['measurement'].append(record['_measurement'])
#             # table_map['value'].append(record['tagname1'])
#                 table_map[key].append(value)
#     df = pd.DataFrame(table_map)
#     df.dropna(inplace=True)
#     df.to_csv(args.local_dir+'/'+args.file_name, index=False)
# df = pd.read_csv("github/data-connectors/influxdb_connector/influxdb_test.csv")
# fields = []
# for index, row in df.iterrows():
#     for i in range(num_col):
#         if not row[i] or pd.isna(row[i]):
#             if i == 0:
#                 val = '2000-01-02'
#             elif i == 9 or i == 10:
#                 val = 3
#             elif i == 11:
#                 val = 'None'
#             elif 1 <= i <= 8:
#                 val = 0.0
#         else:
#             if i == 0:
#                 val = str(row[i])
#             elif i == 9 or i == 10:
#                 val = int(row[i])
#             elif i == 11:
#                 val = str(row[i])
#             elif 1 <= i <= 8:
#                 val = float(row[i])
#         fields.append((columns[i],val))
# idx = 0
# print(fields[:50])
'''
columns = df.columns
num_col = len(columns)
for idx, row in df.iterrows():
    point = (
    Point("anomaly") \
    .time(row[columns[0]]) \
    .field(columns[1], row[columns[1]]) \
    .field(columns[2], row[columns[2]]) \
    .field(columns[3], row[columns[3]]) \
    .field(columns[4], row[columns[4]]) \
    .field(columns[5], row[columns[5]]) \
    .field(columns[6], row[columns[6]]) \
    .field(columns[7], row[columns[7]]) \
    .field(columns[8], row[columns[8]]) \
    .field(columns[9], row[columns[9]]) \
    .field(columns[10], row[columns[10]]) \
    .field(columns[11], row[columns[11]]) \
    )
    print('writing row {idx}')
    write_api.write(bucket=bucket, org="kris.pan@cnvrg.io", record=point)
    time.sleep(0.01)
'''
#     idx += num_col
# for row in data:
#     print(row)
#     for i in len(row):
#         if len(row[i]) < 1:
#             if i == 1:
                
#     point = (
#     Point("measurement") \
#     .time(row[0]) \
#     .field('Accelerometer1RMS', row[1]) \
#     .field('Accelerometer2RMS', row[2]) \
#     .field('Current', row[3]) \
#     .field('Pressure', row[4]) \
#     .field('Temperature', row[5]) \
#     .field('Thermocouple', row[6]) \
#     .field('Voltage', row[7]) \
#     .field('VolumeFlowRateRMS', row[8]) \
#     .field('anomaly', row[9]) \
#     .field('changepoint', row[10]) \
#     .field('status', row[11])
#     )
#     write_api.write(bucket=bucket, org="kris.pan@cnvrg.io", record=point)


# for value in range(len(data)):
#   point = (
#     Point("measurement1")
#     .tag("tagname1", "tagvalue1")
#     .field("field1", value)
#   )
#   write_api.write(bucket=bucket, org="kris.pan@cnvrg.io", record=point)
#   time.sleep(1) # separate points by 1 second

# client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
# query_api = client.query_api()
# # TODO validate bucket and range 
# query = 'from(bucket: "' + bucket + '")\n |> range(start:2017-01-01T00:00:00Z)'
# tables = query_api.query(query, org=org)
# table_map = defaultdict(list)

# for table in tables:
#     for record in table.records:
#         print(record)
    # TODO parse all columns
    # for record in table.records:
    #     print(record)
        # print(type(record))
        # print(record)
# print(table_map[:5])
        
        # for key, value in record.items():
        # table_map['time'].append(record['_time'])
        # table_map['measurement'].append(record['_measurement'])
        # table_map['value'].append(record['tagname1'])
            # table_map[key].append(value)
# df = pd.DataFrame(table_map)
# df.dropna(inplace=True)
# df.to_csv(args.local_dir+'/'+args.file_name, index=False)


# for metric in a:
#     print(metric)
#     print('ok')
#     print(metric[1])
#     influx_metric = [{
#         'measurement': 'your_measurement',
#         'time': metric[0],
#         'fields': {
#              'value': metric[1]
#         }
#     }]
#     db.write_points(influx_metric)

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
        args.org = os.environ.get('INFLUXDB_ORG')
    if args.bucket.lower() == 'secret':
        args.bucket = os.environ.get('INFLUXDB_BUCKET')
    
    # TODO conncetion unit test
    client = influxdb_client.InfluxDBClient(url=args.url, token=args.token, org=args.org)
    query_api = client.query_api()
    # TODO validate bucket and range 
    if args.range_start.lower() != 'none':
        query = 'from(bucket: "' + args.bucket + '")\n |> range(start:' + args.range_start + ')'
    else:
        query = 'from(bucket: "' + args.bucket + '")\n |> range(start:2020-01-01T00:00:00Z)'
    tables = query_api.query(query, org=args.org)
    table_map = defaultdict(list)

    for table in tables:
        # TODO parse all columns
        for record in table.records:
            for key, value in record.items():
            # table_map['time'].append(record['_time'])
            # table_map['measurement'].append(record['_measurement'])
            # table_map['value'].append(record['tagname1'])
                table_map[key].append(value)
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
'''
