.. include:: <mmlalias.txt>


Grafana
=======

.. contents::
   :local:

About
-----

* `About Grafana
  <https://grafana.com/docs/grafana/latest/introduction/>`__

Installation
------------

* `Install Grafana
  <https://grafana.com/docs/grafana/latest/setup-grafana/installation/redhat-rhel-fedora/>`__

  |longrightarrow| `Install Grafana on RHEL or Fedora
  <https://grafana.com/docs/grafana/latest/setup-grafana/installation/redhat-rhel-fedora/>`__

.. code-block:: console

   # systemctl enable grafana-server.service    # optional
   # systemctl start grafana-server.service 

Gosh: Server Listens On Wildcard Interface
------------------------------------------

.. attention::

   To let the NSA in, the default config lets everybody in. This is
   bad. **Big fat minus!**

.. code-block:: console

   # netstat -antp
   ...
   tcp6       0      0 :::3000                 :::*                    LISTEN      384735/grafana      
   ...

In the ``/etc/grafana/grafana.ini``, find the following line:

.. code-block:: console

   # The ip address to bind to, empty will bind to all interfaces
   ;http_addr =

and change it to

.. code-block:: console

   http_addr = 127.0.0.1

Restart

.. code-block:: console

   # systemctl restart grafana.service

Better

.. code-block:: console

   # netstat -antp
   ...
   tcp        0      0 127.0.0.1:3000          0.0.0.0:*               LISTEN      388016/grafana      
   ...

.. sidebar::

   To configure HTTPS, read `Set up Grafana HTTPS for secure web
   traffic
   <https://grafana.com/docs/grafana/latest/setup-grafana/set-up-https/>`__

Dashboards
----------

* `Build your first dashboard
  <https://grafana.com/docs/grafana/latest/getting-started/build-first-dashboard/>`__

Most if not all functionality is available through
http://localhost:3000. Based on a plugin system, many plugins are
available through the base installation. Other plugins might be
needed; even MQTT is available initially, though.

Grafana's company is represented on Github;
https://github.com/grafana.

