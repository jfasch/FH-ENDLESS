The Datalogger
==============

.. contents::
   :local:

Sinks
-----

Sink Interface
..............

.. autoclass:: endless.sink.Sink
   :members:

Mock
....

.. autoclass:: endless.sink_mock.MockSink
   :members:
   :undoc-members:
   :special-members: __init__

MQTT Sink
.........

.. autoclass:: endless.sink_mqtt.MQTTSink
   :members:
   :undoc-members:
   :special-members: __init__

Composite Sink
..............

.. autoclass:: endless.sink_composite.CompositeSink
   :members:
   :undoc-members:
   :special-members: __init__

Sources
-------

Source Interface
................

.. autoclass:: endless.source.Source
   :members:
   :undoc-members:
   :special-members: __init__

Mock
....

.. autoclass:: endless.source_mock.MockSource
   :members:
   :undoc-members:
   :special-members: __init__

CAN Source
..........

.. autoclass:: endless.source_can.CANSource
   :members:
   :undoc-members:
   :special-members: __init__

MQTT Source
...........

.. autoclass:: endless.source_mqtt.MQTTSource
   :members:
   :undoc-members:
   :special-members: __init__

Sample Datalogger Application
-----------------------------

.. literalinclude:: ../../Raspi/bin/data-logger.py
   :language: python
   :caption: :download:`../../Raspi/bin/data-logger.py`
