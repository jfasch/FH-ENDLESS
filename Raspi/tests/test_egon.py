from egon import egon
from endless.sample import Sample
from endless.sample_filter import SampleFilter
from endless.can_util import CANFrame
from endless.interfaces import SampleInlet, Control
from endless.runner import Runner, StopRunning
from endless.sample_receiver import SampleReceiver, have_n_samples

import pytest
from datetime import datetime
import struct
import json


@pytest.mark.asyncio
async def test_canframe_to_humtemp():
    sensor_0x33 = egon.HumidityTemperatureSensor(can_id=0x33, tag='CAN@0x33', timestamps=(datetime(2024, 5, 2, 10, 11,  7),))
    sensor_0x34 = egon.HumidityTemperatureSensor(can_id=0x34, tag='CAN@0x34', timestamps=(datetime(2024, 5, 2, 10, 11, 15),))

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

@pytest.mark.asyncio
async def test_humtemp_to_json():
    class MyJSONConsumer(SampleInlet):
        async def consume_sample(self, sample):
            self.sample = sample

    json_consumer = MyJSONConsumer()
    humtemp2json = SampleFilter(egon.transform_hum_temp_to_json)
    
    humtemp2json.sample_out.connect(json_consumer)

    # inject a humidity/temperature sample
    await humtemp2json.sample_in.consume_sample(
        Sample(
            tag='name',
            timestamp=datetime(2024, 4, 17, 17, 6),
            data=egon.HumidityTemperature(
                humidity=23.3,
                temperature=37.5,
            ),
        )
    )

    assert json_consumer.sample.tag == 'name'
    assert json_consumer.sample.timestamp == datetime(2024, 4, 17, 17, 6)
    assert type(json_consumer.sample.data) is bytes

    json_structure = json.loads(json_consumer.sample.data)
    assert len(json_structure) == 2
    assert json_structure['humidity'] == pytest.approx(23.3)
    assert json_structure['temperature'] == pytest.approx(37.5)

@pytest.mark.asyncio
async def test__humtemp_sample__to__control():
    class MyControl(Control):
        async def adapt(self, timestamp, value):
            self.timestamp = timestamp
            self.value = value

    ctl = MyControl()
    sample_controller = egon.HumidityTemperature2Control()
    sample_controller.control.connect(ctl)

    # inject a humidity/temperature sample
    await sample_controller.sample_in.consume_sample(
        Sample(
            tag='name',
            timestamp=datetime(2024, 4, 17, 17, 6),
            data=egon.HumidityTemperature(
                humidity=23.3,
                temperature=37.5,
            ),
        )
    )

    assert ctl.timestamp == datetime(2024, 4, 17, 17, 6)
    assert ctl.value == pytest.approx(37.5)
