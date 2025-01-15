Test Setup
==========

.. contents::
   :local:

Software
--------

Getting
.......

.. code-block:: console

   $ git clone https://github.com/jfasch/FH-ENDLESS.git

Virtual Environment
...................

* Create virtual environment, and activate it

  .. code-block:: console
  
     $ python -m venv ~/My-Environments/endless
     $ . ~/My-Environments/endless/bin/activate
     (endless) $

* Install requirements

  .. code-block:: console

     (endless) $ cd FH-ENDLESS/              # repo root
     (endless) $ python -m pip install -r requirements.txt

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

   **Unless they are in loopback mode, CAN controllers do not see what
   they send. A receiving application will not see what the sender is
   sending.**

Configuration File
..................

A configuration file defines components and their
interconnections. That network is subject to frequent change. Check if
the configuration fits your situation; for example, the ``CAN_IFACE``
and ``MQTT_ADDR`` variables probably need tuning, as well as CAN IDs,
probably.

.. literalinclude:: ../../Raspi/src/endless/conf/project_1/project_1.conf
   :caption: :download:`project_1.conf (download)
             <../../Raspi/src/endless/conf/project_1/project_1.conf>`
   :language: python

Run Application
...............

.. code-block:: console

   $ cd <FH-ENDLESS>/Raspi                   # subdir Raspi/ of repository root
   $ export PYTHONPATH=$(pwd)/src:$PYTHONPATH

.. code-block:: console

   $ bin/run-components.py --help
   ... read ...
   $ bin/run-components.py --configfile conf/egon.conf
   
``MC-HumTempSensor/``: Sensors On CAN IDs ``0x33`` and ``0x34``
---------------------------------------------------------------

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

Sensor On ``0x33``
..................

.. code-block:: console

   $ ./can-hum-temp-sensor.py --can-interface can0 --can-id 0x33 \
          --interval 1500 \
	  --amplitude-temperature 15 \
	  --hz-temperature 0.2 \
	  --phase-shift-temperature '0.3*pi' \
	  --vertical-shift-temperature 30 \
	  --amplitude-humidity 5 \
	  --hz-humidity 0.5 \
	  --phase-shift-humidity pi/2 \
	  --vertical-shift-humidity 80

Optional: Sensor On ``0x34``
............................

No sensor outage detection is implemented, so it is safe to not start
a second sensor. However, we use to at least publish values from
``0x34`` on a dedicated MQTT topic. If you want to see samples there,
start a second instance of the sensor. For example,

.. code-block:: console

   $ ./can-hum-temp-sensor.py --can-interface can0 --can-id 0x34 \
          --interval 10 \
	  --amplitude-temperature 1500 \
	  --hz-temperature 100 \
	  --phase-shift-temperature 0 \
	  --vertical-shift-temperature 30000 \
	  --amplitude-humidity 5 \
	  --hz-humidity 0.5 \
	  --phase-shift-humidity pi/2 \
	  --vertical-shift-humidity 80

Note that a 10 millisecond sample interval could be a bit too
optimistic - it is a performance test for the application and
connected components like MQTT and databases.

``MC-Switches/``: Actor On CAN ID ``0x40``
------------------------------------------ 

.. code-block:: console

   $ cd <FH-ENDLESS>/MC-Switches/            # subdir MC-Switches/ of repository root
   $ ./can-switches.py --help
   ... read ...
   $ ./can-switches.py --can-interface can0 --can-id 0x40
   16 switches available:
     0: OFF
     1: OFF
     2: OFF
     3: OFF
     4: OFF
     5: OFF
     6: OFF
     7: OFF
     8: OFF
     9: OFF
     10: OFF
     11: OFF
     12: OFF
     13: OFF
     14: OFF
     15: OFF
   ... prints switch actions as they occur ...
