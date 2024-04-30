import datetime

# would rather use @dataclass(frozen=True), but that doesn't let me
# check that timestamps have type datetime.datetime. or does it?

class Sample:
    __slots__ = (
        '_tag',
        '_timestamp',
        '_data',
    )

    def __init__(self, tag, timestamp, data):
        if type(timestamp) is not datetime.datetime:
            raise RuntimeError(f'timestamp {timestamp} must be datetime.datetime (was {type(timestamp)})')

        self._tag = tag
        self._timestamp = timestamp
        self._data = data

    @property
    def tag(self): return self._tag
        
    @property
    def timestamp(self): return self._timestamp
        
    @property
    def data(self): return self._data
