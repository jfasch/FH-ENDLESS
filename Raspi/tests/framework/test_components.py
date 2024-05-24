from endless.framework.component import Component
from endless.framework.errorhandler import ErrorHandler
from endless.framework.source_mock import MockSource
from endless.framework.sample_receiver import SampleReceiver, have_n_samples
from endless.framework.runner import Runner, StopRunning
from endless.framework.async_util import mock_timestamps_async

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
    sink = SampleReceiver(cond=cond)

    source.sample_out.connect(sink.sample_in)

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
