from endless.source_mock import MockSource
from endless.sink_mock import MockSink
from endless.errorhandler_mock import MockErrorHandler
from endless.runner import Runner
from endless import async_util

import pytest
from datetime import datetime, timedelta


@pytest.mark.asyncio
async def test_non_endless_exception():
    def errorfunc(timestamp):
        raise RuntimeError('boom')

    source = MockSource(name='name', 
                        timestamps=async_util.mock_timestamps(start=datetime(2024, 3, 20, 15, 36), 
                                                              interval=timedelta(seconds=1)),
                        temperature=errorfunc)
    sink = MockSink()
    source.connect(sink)

    errorhandler = MockErrorHandler()

    try:
        async with Runner(sources=[source], sinks=[sink], errorhandler=errorhandler):
            pass
    except* RuntimeError:            # terminates all
        pass

    error = errorhandler.errors[0]   # and is reported

    assert type(error.exc_value) is RuntimeError
    assert str(error.exc_value) == 'boom'
    assert error.exc_type is RuntimeError
    assert error.exc_traceback is not None
