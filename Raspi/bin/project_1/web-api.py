#!/usr/bin/env python

from endless.project_1.types import HumidityTemperature
from endless.project_1.dbus_interfaces import HumidityTemperatureHistory

from endless.framework.dbus_interfaces import Counter, HighLowConfig

from fastapi import FastAPI
from pydantic import BaseModel

from datetime import datetime


DBUS_SERVER_BUSNAME = 'org.project_1.Things'


switch_counter_proxy = Counter.new_proxy(DBUS_SERVER_BUSNAME, '/switch_counter')
hysteresis_config_proxy = HighLowConfig.new_proxy(DBUS_SERVER_BUSNAME, '/hysteresis_config')
measurements_controllerA_proxy = HumidityTemperatureHistory.new_proxy(DBUS_SERVER_BUSNAME, '/measurements_controllerA')
measurements_controllerB_proxy = HumidityTemperatureHistory.new_proxy(DBUS_SERVER_BUSNAME, '/measurements_controllerB')

app = FastAPI()

@app.get('/api/switch/counter')
async def switch_counter() -> int: 
    return await switch_counter_proxy.GetCount()

def dbus_to_web_measurements(dbus_measurements):
    web_measurements = []
    for posix_timestamp, (humidity, temperature) in dbus_measurements:
        web_measurements.append((datetime.fromtimestamp(posix_timestamp), HumidityTemperature(humidity, temperature)))
    return web_measurements

@app.get('/api/controllerA/measurements')
async def controllerA_measurements() -> list[tuple[datetime, HumidityTemperature]]: 
    return dbus_to_web_measurements(await measurements_controllerA_proxy.GetLastMeasurements())

@app.get('/api/controllerB/measurements')
async def controllerB_measurements() -> list[tuple[datetime, HumidityTemperature]]: 
    return dbus_to_web_measurements(await measurements_controllerB_proxy.GetLastMeasurements())

@app.post('/api/hysteresis/config/high')
async def hyst_set_high(value: float):
    await hysteresis_config_proxy.SetHigh(value)

@app.post('/api/hysteresis/config/low')
async def hyst_set_low(value: float):
    await hysteresis_config_proxy.SetLow(value)

@app.get('/api/hysteresis/config/show')
async def hyst_show() -> tuple[float, float]:     # low, high
    low, high = await hysteresis_config_proxy.Show()
    return low, high
