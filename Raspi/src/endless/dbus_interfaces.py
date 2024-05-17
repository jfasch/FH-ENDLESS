from . import interfaces

import sdbus


class Counter(
    sdbus.DbusInterfaceCommonAsync,
    interface_name='org.endless.Counter'
):
    def __init__(self, counter:interfaces.Counter|None = None):
        super().__init__()
        self.counter = counter

    @sdbus.dbus_method_async(
        result_signature='t',     # uint64
    )
    async def GetCount(self) -> int:
        assert self.counter
        return await self.counter.get_count()
