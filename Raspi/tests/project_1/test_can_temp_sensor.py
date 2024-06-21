from endless.project_1.can_temp_sensor import CAN_TemperatureSensor
from endless.framework.sample_receiver import SampleReceiver, have_n_samples
from endless.framework.runner import Runner, StopRunning

import pytest
from datetime import datetime
import struct


@pytest.mark.asyncio
async def test_canframe_to_humtemp():
    sensor_0x42 = CAN_TemperatureSensor(can_id=0x42, tag='CAN@0x42', timestamps=(datetime(2024, 6, 21, 11, 20, 4),))

    one_ready, cond = have_n_samples(1)
    sample_sink = SampleReceiver(cond)

    sensor_0x42.sample_out.connect(sample_sink.sample_in)

    async with Runner((sensor_0x42, sample_sink)):
        payload_0x42 = struct.pack('<q', 37500)
        await sensor_0x42.can_in.handle_frame(0x42, payload_0x42)

        await one_ready
        raise StopRunning

    assert sample_sink.collected_samples[0].tag == 'CAN@0x42'
    assert sample_sink.collected_samples[0].timestamp == datetime(2024, 6, 21, 11, 20, 4)
    assert sample_sink.collected_samples[0].data == pytest.approx(37.5)
