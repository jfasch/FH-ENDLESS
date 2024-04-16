import abc


class Inlet(abc.ABC):
    @abc.abstractmethod
    async def consume_sample(self, sample):
        raise NotImplementedError

