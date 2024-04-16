from endless.source_mock import MockSource
from endless.sink_mock import MockSink, have_n_samples
from endless.runner import Runner, StopRunning
from endless.async_util import mock_timestamps_async
from endless.errors import EndlessException
from endless.errorhandler import ErrorHandler

import pytest
from datetime import datetime, timedelta


class _MockErrorHandler(ErrorHandler):
    def __init__(self):
        super().__init__()
        self.exceptions = []
    async def report_exception(self, e):
        self.exceptions.append(e)

@pytest.mark.asyncio
async def test_error_during_runtime__non_endless_exception():
    def errorfunc(timestamp):
        raise RuntimeError('boom!')           # non-"endless" exception

    source = MockSource(name='name', 
                        timestamps=mock_timestamps_async(
                            start=datetime(2024, 4, 12, 10, 41), 
                            interval=timedelta(seconds=1)),
                        data=errorfunc)

    have_1000, cond = have_n_samples(1000)  # awaiting 1000, though we won't even see 1
    sink = MockSink(cond=cond)

    source.outlet.connect(sink.inlet)

    errorhandler = _MockErrorHandler()

    try:
        async with Runner((source, sink), errorhandler=errorhandler):
            await have_1000
            pass
    except* RuntimeError: # exception passes through, terminates all (cancelling have_1000)
        pass

    exception = errorhandler.exceptions[0]   # and is reported

    assert type(exception) is RuntimeError
    assert str(exception) == 'boom!'

@pytest.mark.asyncio
async def test_error_during_runtime__endless_error():
    first_call = True

    def errorfunc(timestamp):
        nonlocal first_call
        if first_call:
            first_call = False
            raise EndlessException('boom!')         # "endless" exception
        
        return 42

    source = MockSource(name='name', 
                        timestamps=mock_timestamps_async(
                            start=datetime(2024, 4, 12, 10, 41), 
                            interval=timedelta(seconds=1)),
                        data=errorfunc)

    # awaiting 10 which we see because an EndlessException does *not* terminate us
    have_10, cond = have_n_samples(10)
    sink = MockSink(cond=cond)

    source.outlet.connect(sink.inlet)

    errorhandler = _MockErrorHandler()

    async with Runner((source,sink), errorhandler=errorhandler) as runner:
        await have_10
        raise StopRunning

    exception = errorhandler.exceptions[0]   # and is reported

    assert type(exception) is EndlessException
    assert str(exception) == 'boom!'

    assert len(sink.collected_samples) >= 10
    for sample in sink.collected_samples:
        assert sample.data == 42

def test_errorhandler_lifetime():
    assert False
