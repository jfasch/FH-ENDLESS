from endless.project_1.hum_temp_control import HumidityTemperature2Control
from endless.project_1.types import HumidityTemperature

from endless.framework.interfaces import Control
from endless.framework.sample import Sample

import pytest
from datetime import datetime


@pytest.mark.asyncio
async def test__humtemp_sample__to__control():
    class MyControl(Control):
        async def adapt(self, timestamp, value):
            self.timestamp = timestamp
            self.value = value

    ctl = MyControl()
    sample_controller = HumidityTemperature2Control()
    sample_controller.control.connect(ctl)

    # inject a humidity/temperature sample
    await sample_controller.sample_in.consume_sample(
        Sample(
            tag='name',
            timestamp=datetime(2024, 4, 17, 17, 6),
            data=HumidityTemperature(
                humidity=23.3,
                temperature=37.5,
            ),
        )
    )

    assert ctl.timestamp == datetime(2024, 4, 17, 17, 6)
    assert ctl.value == pytest.approx(37.5)
