Using InfluxDB
==============

.. contents::
   :local:

.. sidebar::

   * Guided through by
     https://docs.influxdata.com/influxdb/v2/get-started/setup/
   * Server Installation:
     https://docs.influxdata.com/influxdb/v2/install/

Server Setup
------------

Installation
............

Fedorishly, I did

.. code-block:: console

   $ wget --output-document=$HOME/tmp/influxdb2-2.7.4-1.x86_64.rpm https://dl.influxdata.com/influxdb/releases/influxdb2-2.7.4-1.x86_64.rpm
   $ sudo rpm -hiv $HOME/tmp/influxdb2-2.7.4-1.x86_64.rpm
   $ rm $HOME/tmp/influxdb2-2.7.4-1.x86_64.rpm

(There is no download fingerprint supplied, which raised my eyebrows a
bit.)

Server Security
...............

For the paranoid ... err, security aware ... the following is the
default configuration,

* Cleartext HTTP is used
* Server opens port 8086, listening on *all* interfaces

.. code-block:: console

   # netstat -antp
   ...
   tcp6       0      0 :::8086                 :::*                    LISTEN      620488/influxd      
   ...

Add the following line to ``/etc/influxdb/config.toml``,

.. code-block:: console
   :caption:``/etc/influxdb/config.toml``

   # "LOCALHOST ONLY" should be the default but isn't                                                                                                                                            http-bind-address = "127.0.0.1:8086"

Startup
.......

Finally, start the service and optionally *enable* it at boot,

.. code-block:: console

   # systemctl start influxdb.service 
   # systemctl enable influxdb.service 

Paranoidly check network situation,

.. code-block:: console

   # netstat -antp
   ...
   tcp        0      0 127.0.0.1:8086          0.0.0.0:*               LISTEN      620804/influxd  
                       ^^^^^^^^^
   ...

CLI Setup
---------

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

Next ...
--------

View Server Configuration
.........................

.. code-block:: console

   $ influx server-config
   Error: failed to retrieve config: 401 Unauthorized: unauthorized access

Viewing the config is a "server config command",
obviously. https://docs.influxdata.com/influxdb/v2/reference/config-options/
says

..

  Server configuration commands require an Operator token.

Create operator token:
https://docs.influxdata.com/influxdb/v2/admin/tokens/#operator-token

Confusion, 

..

  Operator tokens are created in the InfluxDB setup process. To create
  an operator token manually with the InfluxDB UI, api/v2 API, or influx
  CLI after the setup process is completed, you must use an existing
  Operator token.

Where's the pre-existing operator token?

Stop here, and point browser to ``http://localhost:8086``

Initial Configuration
---------------------

* Create initial setup. Mine is

  * Username: ``jfasch``
  * Password: ``jfasch777``
  * Initial organization name: ``faschingbauer``
  * Initial bucket name: ``my-bucket``

  Here the "Operator token" miracle is solved; mine is
  ``Wor6XXn5emD6DpKPkHHt5_UMqbUb9N0_EW_SY9L29bIyjpe56E7lgxK0Ce4XkQNWxjvpyrzfS0OJi3D5xkl5CA==``
  (*Note* that this is not an information disclosure as you don't
  reach my database from outside my own computer)

Python Client
-------------

Click through http://localhost:8086/orgs/218d89cad71fac28/new-user-setup/python

Another token, an "all-access token" (created as I click through), is
needed to authenticate a Python client program against the database,

.. code-block:: console

   $ export INFLUXDB_TOKEN=b9JzaHkTEQdmivCxAMwgHWDLrFnrigq7lz26_-w5dRpXcydDM77M60GRz5WnpMUoJv9xasAuAVnwy9__Bh8QzQ==

As they say,

.. 

   Creating an all-access token is not the best security practice! We
   recommend you delete this token in the Tokens page after setting
   up, and create your own token with a specific set of permissions
   later.

