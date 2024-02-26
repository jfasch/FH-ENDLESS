async def enumerate(aiterable, start=0):
    async for item in aiterable:
        yield start, item
        start += 1
