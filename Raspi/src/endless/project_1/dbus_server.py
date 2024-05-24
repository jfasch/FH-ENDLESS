from .dbus_interfaces import HumidityTemperatureHistory

from endless.framework import dbus_interfaces
from endless.framework.receptacle import receptacle, ONE
from endless.framework.facet import facet
from endless.framework.component import LifetimeComponent
from endless.framework.interfaces import Counter, SampleList, HighLowConfig

import sdbus
import asyncio


@receptacle('switch_counter', Counter, multiplicity=ONE)
@receptacle('hysteresis_config', HighLowConfig, multiplicity=ONE)
@receptacle('measurements_controllerA', SampleList, multiplicity=ONE)
@receptacle('measurements_controllerB', SampleList, multiplicity=ONE)
class DBusServer(LifetimeComponent):
    def __init__(self, busname):
        super().__init__(self._run)
        self.busname = busname
        
    async def _run(self):
        await sdbus.request_default_bus_name_async(self.busname)

        switch_counter_dbus_object = dbus_interfaces.Counter(self._switch_counter)
        switch_counter_dbus_object.export_to_dbus('/switch_counter')

        measurements_controllerA_dbus_object = HumidityTemperatureHistory(self._measurements_controllerA)
        measurements_controllerA_dbus_object.export_to_dbus('/measurements_controllerA')

        measurements_controllerB_dbus_object = HumidityTemperatureHistory(self._measurements_controllerB)
        measurements_controllerB_dbus_object.export_to_dbus('/measurements_controllerB')

        hysteresis_config_dbus_object = dbus_interfaces.HighLowConfig(self._hysteresis_config)
        hysteresis_config_dbus_object.export_to_dbus('/hysteresis_config')

        while True: # hmm. can't I await something from sdbus?
            await asyncio.sleep(10000)
        

