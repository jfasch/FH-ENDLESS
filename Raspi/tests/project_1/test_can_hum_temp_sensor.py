from endless.project_1.can_hum_temp_sensor import CAN_HumidityTemperatureSensor
from endless.framework.sample_receiver import SampleReceiver, have_n_samples
from endless.framework.runner import Runner, StopRunning

import pytest
from datetime import datetime
import struct


@pytest.mark.asyncio
async def test_canframe_to_humtemp():
    sensor_0x33 = CAN_HumidityTemperatureSensor(can_id=0x33, tag='CAN@0x33', timestamps=(datetime(2024, 5, 2, 10, 11,  7),))
    sensor_0x34 = CAN_HumidityTemperatureSensor(can_id=0x34, tag='CAN@0x34', timestamps=(datetime(2024, 5, 2, 10, 11, 15),))

    two_ready, cond = have_n_samples(2)
    sample_sink = SampleReceiver(cond)

    sensor_0x33.sample_out.connect(sample_sink.sample_in)
    sensor_0x34.sample_out.connect(sample_sink.sample_in)

    async with Runner((sensor_0x33, sensor_0x34, sample_sink)):
        payload_0x33 = struct.pack('<iI', int(-42.7*10), int(83.2*10))
        await sensor_0x33.can_in.handle_frame(0x33, payload_0x33)
        await sensor_0x34.can_in.handle_frame(0x33, payload_0x33) # ignored

        payload_0x34 = struct.pack('<iI', int(666.4*10), int(50.1*10))
        await sensor_0x33.can_in.handle_frame(0x34, payload_0x34)
        await sensor_0x34.can_in.handle_frame(0x34, payload_0x34) # ignored

        await two_ready
        raise StopRunning

    assert sample_sink.collected_samples[0].tag == 'CAN@0x33'
    assert sample_sink.collected_samples[0].timestamp == datetime(2024, 5, 2, 10, 11, 7)
    assert sample_sink.collected_samples[0].data.temperature == pytest.approx(-42.7)
    assert sample_sink.collected_samples[0].data.humidity == pytest.approx(83.2)

    assert sample_sink.collected_samples[1].tag == 'CAN@0x34'
    assert sample_sink.collected_samples[1].timestamp == datetime(2024, 5, 2, 10, 11, 15)
    assert sample_sink.collected_samples[1].data.temperature == pytest.approx(666.4)
    assert sample_sink.collected_samples[1].data.humidity == pytest.approx(50.1)
