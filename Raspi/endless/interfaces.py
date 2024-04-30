import abc


class Inlet(abc.ABC):
    @abc.abstractmethod
    async def consume_sample(self, sample):
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
