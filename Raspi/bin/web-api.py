#!/usr/bin/env python

from endless import dbus_interfaces

from fastapi import FastAPI


switch_counter_proxy = dbus_interfaces.Counter.new_proxy('org.endless.Things', '/switch_counter')

app = FastAPI()

@app.get("/switch_counter")
async def switch_counter() -> int: 
    return await switch_counter_proxy.GetCount()
