import datetime

# would rather use @dataclass(frozen=True), but that doesn't let me
# check that timestamps have type datetime.datetime. or does it?

class Sample:
    __slots__ = (
        '_name',
        '_timestamp',
        '_temperature',
    )

    def __init__(self, name, timestamp, temperature):
        if type(timestamp) is not datetime.datetime:
            raise RuntimeError(f'{timestamp} must be datetime.datetime')

        self._name = name
        self._timestamp = timestamp
        self._temperature = temperature

    @property
    def name(self): return self._name
        
    @property
    def timestamp(self): return self._timestamp
        
    @property
    def temperature(self): return self._temperature
        
    def __eq__(self, rhs):
        '''for tests only. we are comparing temperature (float) for
        equality, and the user is supposed to know that - and pass a pytest.approx object'''

        return self._name == rhs._name and self._timestamp == rhs._timestamp and self._temperature == rhs._temperature
