import abc


class Inlet(abc.ABC):
    @abc.abstractmethod
    async def consume_sample(self, sample):
        raise NotImplementedError

class Switch(abc.ABC):
    @abc.abstractmethod
    async def set_state(self, state):
        raise NotImplementedError
    
