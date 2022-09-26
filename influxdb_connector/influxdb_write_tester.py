import os
import argparse
import pandas as pd
from collections import defaultdict
# from cnvrgv2 import Cnvrg
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

cnvrg_workdir = os.environ.get("CNVRG_WORKDIR", "/cnvrg")
url = "placeholder"
org =  "placeholder"
token = "placeholder"
bucket = "placeholder"
# writing data to influxdb api
client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

df = pd.read_csv("github/data-connectors/influxdb_connector/1new.csv", sep=';')
df = df.drop(['anomaly', 'changepoint'], axis=1)

df['datetime'] = pd.to_datetime(df['datetime'], errors='ignore')
df['datetime'] = df['datetime'].fillna(value=pd.to_datetime('2022-09-01 01:01:01'))
df[['Accelerometer1RMS','Accelerometer2RMS','Current','Pressure','Temperature','Thermocouple','Voltage','Volume Flow RateRMS']] = \
    df[['Accelerometer1RMS','Accelerometer2RMS','Current','Pressure','Temperature','Thermocouple','Voltage','Volume Flow RateRMS']].fillna(value=0.0)
df[['anomaly','changepoint']] = df[['anomaly','changepoint']].fillna(3)
df['status'] = df['status'].fillna('None')
convert_dict = {'anomaly': int,'changepoint': int, 'status': str}
df = df.astype(convert_dict)
df = df.rename(columns={"datetime": "time"})
# print(df.dtypes)
write_api = client.write_api(write_options=SYNCHRONOUS)

columns = df.columns
num_col = len(columns)
for idx, row in df.iterrows():
    point = (
    Point("ts") \
    .time(row[columns[0]]) \
    .field(columns[1], row[columns[1]]) \
    .field(columns[2], row[columns[2]]) \
    .field(columns[3], row[columns[3]]) \
    .field(columns[4], row[columns[4]]) \
    .field(columns[5], row[columns[5]]) \
    .field(columns[6], row[columns[6]]) \
    .field(columns[7], row[columns[7]]) \
    .field(columns[8], row[columns[8]]) 
    )
    print('writing row: ', idx)
    write_api.write(bucket=bucket, org="kris.pan@cnvrg.io", record=point)
    time.sleep(0.01)

query_api = client.query_api()
query = 'from(bucket: "' + bucket + '")\n |> range(start: -10y)'
tables = query_api.query(query, org=org)
csv_builder = dict()
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
df = pd.DataFrame(csv_builder)
print(df[:5])


