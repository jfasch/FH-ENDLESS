from endless import dbus_interfaces
from endless.receptacle import receptacle, ONE
from endless.facet import facet
from endless.component import LifetimeComponent
from endless.interfaces import Counter

import sdbus
import asyncio


@receptacle('switch_counter', Counter, multiplicity=ONE)
class DBusServer(LifetimeComponent):
    def __init__(self, busname):
        super().__init__(self._run)
        self.busname = busname
        
    async def _run(self):
        await sdbus.request_default_bus_name_async(self.busname)

        switch_counter_dbus_object = dbus_interfaces.Counter(self._switch_counter)
        switch_counter_dbus_object.export_to_dbus('/switch_counter')

        while True: # hmm. can't I await something from sdbus?
            await asyncio.sleep(10000)
        
