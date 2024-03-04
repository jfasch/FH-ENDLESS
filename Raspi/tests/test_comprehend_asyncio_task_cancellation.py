import pytest
import asyncio


class _MyException(Exception): pass

@pytest.mark.asyncio
async def test_exception_no_group():
    async def error():
        raise _MyException('gosh')

    task = asyncio.create_task(error())

    with pytest.raises(_MyException):
        await task

@pytest.mark.asyncio
async def test_exception_group():
    async def error():
        raise _MyException('gosh')
    async def sleeper():
        await asyncio.sleep(100000)

    async with asyncio.TaskGroup() as tg:
        sleep_task = tg.create_task(sleeper())
        tg.create_task(error())

    assert cancelled.cancelled()
