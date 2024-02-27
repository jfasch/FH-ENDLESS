async def sink_stdout(queue):
    while True:
        name, timestamp_ms, temperature = await queue.get()
        print(name, timestamp_ms, temperature)
