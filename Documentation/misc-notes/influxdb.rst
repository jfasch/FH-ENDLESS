Using InfluxDB
==============

.. contents::
   :local:

Installation
------------

Server
......

.. sidebar::

   * `Server Installation
     <https://docs.influxdata.com/influxdb/v2/install/>`__

Fedorishly, I did

.. code-block:: console

   $ curl --remote-name https://dl.influxdata.com/influxdb/releases/influxdb2-2.7.4-1.x86_64.rpm --output /tmp/influxdb2-2.7.4-1.x86_64.rpm
   $ sudo rpm -ivh influxdb2-2.7.4-1.x86_64.rpm 

(There is no download fingerprint supplied, which raised my eyebrows a
bit.)

Finally, start the service

.. code-block:: console

   $ systemctl start influxdb.service 

(Again raising eyebrows; in the documentation they start the ancient
SysV init script.)

Btw., 

* Data is in ``/var/lib/influxdb/``
* Config is in ``/etc/influxdb/``

CLI
...

.. sidebar::

   * `CLI Installation
     <https://docs.influxdata.com/influxdb/v2/tools/influx-cli/>`__

.. code-block:: console
   :caption: Download ``tar`` file

   $ wget https://dl.influxdata.com/influxdb/releases/influxdb2-client-2.7.3-linux-amd64.tar.gz
   
Eyebrows: look into ``tar`` file, and discover that they don't create
*one single* subdirectory to contain the items. Argh.

.. code-block:: console

   $ mkdir influx-crap
   $ cd influx-crap
   $ tar xf ../influxdb2-client-2.7.3-linux-amd64.tar.gz
