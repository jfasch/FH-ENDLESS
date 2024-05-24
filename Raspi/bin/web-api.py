#!/usr/bin/env python

from egon.types import HumidityTemperature
from egon.dbus_interfaces import HumidityTemperatureHistory
from endless.dbus_interfaces import Counter

from fastapi import FastAPI
from datetime import datetime


switch_counter_proxy = Counter.new_proxy('org.egon.Things', '/switch_counter')
measurements_controllerA_proxy = HumidityTemperatureHistory.new_proxy('org.egon.Things', '/measurements_controllerA')
measurements_controllerB_proxy = HumidityTemperatureHistory.new_proxy('org.egon.Things', '/measurements_controllerB')

app = FastAPI()

@app.get("/switch_counter")
async def switch_counter() -> int: 
    return await switch_counter_proxy.GetCount()

def dbus_to_web_measurements(dbus_measurements):
    web_measurements = []
    for posix_timestamp, (humidity, temperature) in dbus_measurements:
        web_measurements.append((datetime.fromtimestamp(posix_timestamp), HumidityTemperature(humidity, temperature)))
    return web_measurements

@app.get("/measurements_controllerA")
async def measurements_controllerA() -> list[tuple[datetime, HumidityTemperature]]: 
    return dbus_to_web_measurements(await measurements_controllerA_proxy.GetLastMeasurements())

@app.get("/measurements_controllerB")
async def measurements_controllerB() -> list[tuple[datetime, HumidityTemperature]]: 
    return dbus_to_web_measurements(await measurements_controllerB_proxy.GetLastMeasurements())
