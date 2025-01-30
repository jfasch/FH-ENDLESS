Satellite Devices
=================

.. sidebar::

   .. image:: /Egon-Sketch.jpg

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
