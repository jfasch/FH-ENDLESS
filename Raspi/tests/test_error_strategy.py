from endless.source_mock import MockSource
from endless.sink_mock import MockSink, have_n_samples
from endless.runner import Runner
from endless.async_util import mock_timestamps_async
from endless.errorhandler_mock import MockErrorHandler_Lifetime
from endless.errors import EndlessException

import pytest
from datetime import datetime, timedelta


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

    errorhandler = MockErrorHandler_Lifetime()

    try:
        async with Runner((source, sink), errorhandler=errorhandler):
            await have_1000
            pass
    except* RuntimeError: # exception passes through, terminates all (cancelling have_1000)
        pass

    error = errorhandler.collected_errors[0]   # and is reported

    assert type(error.exc_value) is RuntimeError
    assert str(error.exc_value) == 'boom!'
    assert error.exc_type is RuntimeError
    assert error.exc_traceback is not None

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

    errorhandler = MockErrorHandler_Lifetime()

    async with Runner((source,), errorhandler=errorhandler) as runner:
        await have_10
        runner.stop()

    error = errorhandler.collected_errors[0]   # and is reported

    assert type(error.exc_value) is EndlessException
    assert str(error.exc_value) == 'boom!'
    assert error.exc_type is EndlessException
    assert error.exc_traceback is not None

    assert len(sink.collected_samples) >= 10
    for sample in sink.collected_samples:
        assert sample.data == 42
