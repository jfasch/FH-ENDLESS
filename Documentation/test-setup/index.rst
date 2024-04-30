Test Setup
==========

.. contents::
   :local:

Software
--------

Get
...

.. code-block:: console

   $ git clone https://github.com/jfasch/FH-ENDLESS.git

Virtual Environment
...................

* Create virtual environment

  .. code-block:: console
  
     $ python -m venv ~/My-Environments/endless
     $ . ~/My-Environments/endless/bin/activate
     $ (endless)

* Enable it

  .. code-block:: console
  
     $ . ~/My-Environments/endless/bin/activate
     $ (endless)

* Install requirements

  .. code-block:: console

     $ (endless) cd FH-ENDLESS/       # repo root
     $ (endless) python -m pip install -r requirements.txt

CAN Bus
-------

MCSP2515 Hat, And Raspberry Bootloader Config
.............................................

.. sidebar::

   * `Waveshare RS485 CAN HAT
     <https://www.waveshare.com/wiki/RS485_CAN_HAT>`__
   * :doc:`jfasch:trainings/material/soup/linux/hardware/can/20-interfaces`

* In ``/boot/firmware/overlays/README``, search for mention of
  ``mcp2515``
* Add those lines to ``/boot/firmware/config.txt``

  .. code-block:: text

     dtparam=spi=on
     dtoverlay=mcp2515-can0,oscillator=12000000,interrupt=25,spimaxfrequency=2000000

* Reboot
* Check

  .. code-block:: console

     $ ip link show can0
     3: can0: <NOARP,ECHO> mtu 16 qdisc noop state DOWN mode DEFAULT group default qlen 10
         link/can 

CAN Interface Configuration
...........................

You have configured a CAN controller into your system, be it a Pi Hat
or a USB gadget. To communicate, you set at least the bitrate, and up
the interface.

* Determine interface name (we'll use ``can0`` in the following)

  $ ip link show
  ... check for a CAN type interface ...

* Set speed and buffer size

  .. code-block:: console

     # ip link set can0 type can bitrate 500000
     # ip link set can0 txqueuelen 1000

* Up the interface

  .. code-block:: console

     # ip link set can0 up

All-Simulated CAN: ``vcan``
...........................

.. sidebar::

   * :doc:`jfasch:trainings/material/soup/linux/hardware/can/20-interfaces`

.. code-block:: console

   # modprobe vcan
   # ip link add dev mein-test-can type vcan
   # ip link set mein-test-can up

``Raspi/``: The Raspberry Pi Application
----------------------------------------

.. sidebar::

   * :doc:`/Raspi/index`

.. note::

   On a physical CAN bus, do *not* collocate the Pi application and
   the microcontroller mockups *on the same machine*. 

   **CAN controllers do not see what they send!**

Configuration File
..................

Components and their interconnections are subject to frequent
change. Check if it fits your situation; for example, the
``CAN_IFACE`` and ``MQTT_ADDR`` variables probably need tuning.

.. literalinclude:: ../../Raspi/conf/egon.conf
   :caption: :download:`egon.conf (download)
             <../../Raspi/conf/egon.conf>`
   :language: python

Run Application
...............

.. code-block:: console

   $ cd <FH-ENDLESS>/Raspi                   # subdir Raspi/ of repository root
   $ export PYTHONPATH=$(pwd)/$PYTHONPATH

.. code-block:: console

   $ bin/run-components.py --help
   ... read ...
   $ bin/run-components.py --configfile conf/egon.conf
   
``MC-HumTempSensor/``: The Sensor "Application" At CAN ``0x33`` and `0x34``
---------------------------------------------------------------------------

In lack of a real sensor microcontroller (Egon has one), we start a
Python program. It simulates the measurements, and outputs on CAN two
configurable sine curves instead.

.. code-block:: console

   $ cd <FH-ENDLESS>/MC-HumTempSensor/       # subdir MC-HumTempSensor/ of repository root
   $ ./can-hum-temp-sensor.py --help
   ... read ...

Note that the CAN interface, and the controller's CAN ID must match
that of the config file. Take also into respect that the hysteresis
(see config file) has as its input the temperature measurements from
``0x33``.

.. code-block:: console

