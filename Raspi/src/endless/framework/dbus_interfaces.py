from . import interfaces

import sdbus


class Counter(
        sdbus.DbusInterfaceCommonAsync,
        interface_name='org.endless.Counter'
):
    def __init__(self, counter: interfaces.Counter):
        super().__init__()
        self.counter = counter

    @sdbus.dbus_method_async(
        result_signature='t',     # uint64
    )
    async def GetCount(self) -> int:
        assert self.counter
        return await self.counter.get_count()

class HighLowConfig(
        sdbus.DbusInterfaceCommonAsync,
        interface_name='org.endless.HighLowConfig'
):
    def __init__(self, config: interfaces.HighLowConfig):
        super().__init__()
        self.config = config

    @sdbus.dbus_method_async(
        input_signature='d'     # double
    )
    async def SetLow(self, value: float):
        await self.config.set_low(value)

    @sdbus.dbus_method_async(
        input_signature='d'     # double
    )
    async def SetHigh(self, value: float):
        await self.config.set_high(value)

    @sdbus.dbus_method_async(
        result_signature='(dd)'     # double: (low, high)
    )
    async def Show(self):
        low, high = await self.config.show()
        return float(low), float(high)
