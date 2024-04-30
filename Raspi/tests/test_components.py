from endless.component import Component
from endless.errorhandler import ErrorHandler
from endless.source_mock import MockSource
from endless.sink_mock import MockSink, have_n_samples
from endless.runner import Runner, StopRunning
from endless.async_util import mock_timestamps_async

import pytest
from datetime import datetime, timedelta


def test_baseclass_has_errorhandler():
    class MyComponent(Component):
        pass

    comp = MyComponent()
    assert hasattr(comp, 'errorhandler')

    class MyErrorHandler(ErrorHandler):
        def __init__(self): super().__init__()
        def report_exception(self, e): pass

    comp.errors_to(MyErrorHandler())

@pytest.mark.asyncio
async def test_basic_run():
    source = MockSource(
        tag='source', 
        timestamps=mock_timestamps_async(start=datetime(2024, 4, 12, 9, 19), interval=timedelta(seconds=3)), 
        data=36.5)

    have_1, cond = have_n_samples(1)
    sink = MockSink(cond=cond)

    source.outlet.connect(sink.inlet)

    async with Runner((source,sink)) as runner:
        assert source.task is not None
        assert sink.task is not None
        await have_1
        raise StopRunning

    assert source.task is None
    assert sink.task is None

    assert sink.collected_samples[0].tag == 'source'
    assert sink.collected_samples[0].timestamp == datetime(2024, 4, 12, 9, 19)
    assert sink.collected_samples[0].data == pytest.approx(36.5)
