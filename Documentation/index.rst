The ENDLESS Project
===================

.. contents::
   :local:

.. toctree::
   :hidden:

   Raspi/index
   misc-notes/index
   test-setup/index
   yocto/index


The Beginning Of It All
-----------------------

.. image:: Egon-Sketch.jpg
   :scale: 40%

The Raspberry Pi Application
----------------------------

.. sidebar::

   * :doc:`Raspi/index`

In the sketch, this is the node labeled "Raspi". A datalogger,
basically, capable of

* Receiving measurements from various *sources*

  * CAN bus
  * MQTT
  * Random simulated data
  * ... to be continued ...

* sending measurements to various *sinks*

  * MQTT
  * Standard output (aka "console")
  * `InfluxDB <https://docs.influxdata.com/influxdb>`__ to come soon
  * ... to be continued ...

* Triggering actions on numerous kinds of actors

``MC-HumTempSensor/``
---------------------

In the sketch, this resembles one of the nodes labeled "MC". A Python
program that does not produces any real measurements, but generates a
configurable sine wave that it sends out over a CAN interface. It runs
on Linux, either with real CAN hardware, or using a :doc:`Virtual CAN
interface <jfasch:trainings/material/soup/linux/hardware/can/group>`

The "Raspi" node is supposed to pick that up as one of its sources.

``MC-Switches/``
----------------

Another pseudo microcontroller application: a Python program that
operates an array of 16 switches, and listens on a CAN bus for
commands.
