from endless.mqtt import Publisher, MQTT_PublishSampleTagToTopic
from endless.sample import Sample

import pytest
from datetime import datetime


@pytest.mark.asyncio
async def test_basic():
    class MyPublisher(Publisher):
        def __init__(self):
            self.topic = self.message = None
        async def publish(self, topic, message):
            self.topic = topic
            self.message = message

    mqtt_splitter = MQTT_PublishSampleTagToTopic({
        'tag1': 'topic1',
        'tag2': 'topic2',
    })
    my_publisher = MyPublisher()
    
    mqtt_splitter.publisher.connect(my_publisher)

    await mqtt_splitter.inlet.consume_sample(
        Sample(
            tag='tag1',
            timestamp=datetime(2024, 4, 18, 16, 27),
            data=b'payload1',
        )
    )

    assert my_publisher.topic == 'topic1'
    assert my_publisher.message == b'payload1'

    await mqtt_splitter.inlet.consume_sample(
        Sample(
            tag='tag2',
            timestamp=datetime(2024, 4, 18, 16, 29),
            data=b'payload2',
        )
    )

    assert my_publisher.topic == 'topic2'
    assert my_publisher.message == b'payload2'


