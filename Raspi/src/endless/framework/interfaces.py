from .sample import Sample

import abc
from typing import Iterable


class SampleInlet(abc.ABC):
    @abc.abstractmethod
    async def consume_sample(self, sample):
        raise NotImplementedError

class Control(abc.ABC):
    @abc.abstractmethod
    async def adapt(self, timestamp, value):
        raise NotImplementedError

class HighLowConfig(abc.ABC):
    @abc.abstractmethod
    async def set_high(self, value):
        raise NotImplementedError
    @abc.abstractmethod
    async def set_low(self, value):
        raise NotImplementedError
    @abc.abstractmethod
    async def show(self):
        raise NotImplementedError

class Switch(abc.ABC):
    @abc.abstractmethod
    async def set_state(self, state: bool):
        raise NotImplementedError
    
class Publisher(abc.ABC):
    '''MQTT style "publish" interface. Not necessarily coupled to MQTT.'''
    @abc.abstractmethod
    async def publish(self, topic, message):
        '''Publish ``message`` on ``topic``'''
        raise NotImplementedError

class CANInputHandler(abc.ABC):
    '''Handles CAN-style input: binary payload, associated with an CAN ID'''
    @abc.abstractmethod
    async def handle_frame(self, can_id, payload):
        raise NotImplementedError
        
class CANOutputHandler(abc.ABC):
    '''Handles CAN-style output: binary payload, associated with an CAN ID'''
    @abc.abstractmethod
    async def write_frame(self, can_id, payload):
        raise NotImplementedError
        
class Counter(abc.ABC):
    @abc.abstractmethod
    async def get_count(self):
        raise NotImplementedError

class SampleList(abc.ABC):
    @abc.abstractmethod
    async def get_samples(self) -> Iterable[Sample]:
        raise NotImplementedError
