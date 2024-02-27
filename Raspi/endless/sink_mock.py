async def sink_mock(queue, samples):
    while True:
        name, timestamp_ms, temperature = await queue.get()
        samples.append((name, timestamp_ms, temperature))
