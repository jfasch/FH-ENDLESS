from endless.framework.component import Component
from endless.framework.facet import facet
from endless.framework.receptacle import receptacle, ONE
from endless.framework.interfaces import SampleInlet, Control


@facet('sample_in', SampleInlet, (('consume_sample', '_consume_sample'),))
@receptacle('control', Control, multiplicity=ONE)
class HumidityTemperature2Control(Component):
    '''
    * Receives samples via facet ``sample_in``
    * Extracts ``timestamp`` and ``temperature``
    * Adapts connected ``control`` receptacle
    '''
    async def _consume_sample(self, sample):
        await self._control.adapt(timestamp=sample.timestamp, value=sample.data.temperature)

