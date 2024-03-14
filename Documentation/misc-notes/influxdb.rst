Using InfluxDB
==============

.. contents::
   :local:

Installation
------------

.. sidebar::

   Guided through by
   https://docs.influxdata.com/influxdb/v2/get-started/setup/

Server
......

.. sidebar::

   Server Installation:
   https://docs.influxdata.com/influxdb/v2/install/

Fedorishly, I did

.. code-block:: console

   $ wget --output-document=$HOME/tmp/influxdb2-2.7.4-1.x86_64.rpm https://dl.influxdata.com/influxdb/releases/influxdb2-2.7.4-1.x86_64.rpm
   $ sudo rpm -ivh $HOME/tmp/influxdb2-2.7.4-1.x86_64.rpm
   $ rm $HOME/tmp/influxdb2-2.7.4-1.x86_64.rpm

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

   CLI Installation:
   https://docs.influxdata.com/influxdb/v2/tools/influx-cli/

.. code-block:: console
   :caption: Download ``tar`` file

   $ wget --output-document=$HOME/tmp/influxdb2-client-2.7.3-linux-amd64.tar.gz https://dl.influxdata.com/influxdb/releases/influxdb2-client-2.7.3-linux-amd64.tar.gz
   $ tar -t -f $HOME/tmp/influxdb2-client-2.7.3-linux-amd64.tar.gz
   
Argh: the ``tar`` file doesn't have its content in a single
subdirectory which is respectless and unprofessional. Create dedicated
directory, unpack into that.

.. code-block:: console

   $ mkdir ~/tmp/influx-crap
   $ cd ~/tmp/influx-crap
   $ tar -x -f ../influxdb2-client-2.7.3-linux-amd64.tar.gz
   $ ls -l 
   total 24660
   -rwxr-xr-x. 1 jfasch jfasch 25240165 Apr 28  2023 influx
   -rw-r--r--. 1 jfasch jfasch     1067 Apr 28  2023 LICENSE
   -rw-r--r--. 1 jfasch jfasch     2196 Apr 28  2023 README.md
   $ file influx 
   influx: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), statically linked, Go BuildID=hgLwH6zdpMV9xzby8Jfl/mZkurGFHWhWMO3nC3kre/JZi3O3DZG5GLKLHJiw1g/dWjuVh4yaNwx-vlVvxhK, with debug_info, not stripped

A-ha - a statically linked executable. I have
``/home/jfasch/.local/bin`` in ``$PATH``, so copy it there.

.. code-block:: console

   $ cp influx /home/jfasch/.local/bin
   $ influx --help
   ... help screen ...


AAAARGGHHH
----------

The server is listening on the wildcard interface,

.. code-block:: console

   # netstat -antp
   ...
   tcp6       0      0 :::8086                 :::*                    LISTEN      1297/influxd        
   ...

This does not look like I want that (anybody could connect from
outside, which is not a sane default IMO).

Stop it, and fix it before continuing here.
