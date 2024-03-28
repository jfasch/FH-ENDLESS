#!/usr/bin/env python

# code gathered together by clicking through
# http://localhost:8086/orgs/218d89cad71fac28/new-user-setup/python

import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

token = os.environ.get("INFLUXDB_TOKEN")
org = "faschingbauer"
url = "http://localhost:8086"

write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

bucket="my-bucket"

write_api = write_client.write_api(write_options=SYNCHRONOUS)
   
for value in range(5):
  point = (
    Point("measurement1")
    .tag("tagname1", "tagvalue1")
    .field("field1", value)
  )
  write_api.write(bucket=bucket, org="faschingbauer", record=point)
  time.sleep(1) # separate points by 1 second
