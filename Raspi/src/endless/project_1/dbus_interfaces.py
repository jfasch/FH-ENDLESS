from endless.framework.interfaces import SampleList

import sdbus


class HumidityTemperatureHistory(
        sdbus.DbusInterfaceCommonAsync,
        interface_name='org.egon.HumidityTemperatureHistory'
):
    '''From an instance of the ``SampleList`` interface (which is
    passed in the constructor), interpret the samples as carrying
    ``HumidityTemperature`` measurements, and convert them to a DBus
    array of (timestamp, (humidity, temperature)) measurements.
    '''

    def __init__(self, samples:SampleList):
        super().__init__()
        self.samples = samples

    @sdbus.dbus_method_async(
        result_signature='a(d(dd))',        # list[(double posix_timestamp, (double humidity, double temperature))]
    )
    async def GetLastMeasurements(self):
        ret = []

        # note that this is not "async for". samples.get_samples() is
        # async; await it to get a *list of samples* which is a plain
        # iterable (no async).

        for sample in await self.samples.get_samples():
            ret.append((sample.timestamp.timestamp(), (sample.data.humidity, sample.data.temperature)))
        return ret
