The Raspberry Pi Application
============================

.. contents::
   :local:

Installation
------------

.. toctree::
   :hidden:

   packaging

See :ref:`raspi-packaging-installation`

Architecture
------------   

.. sidebar::

   .. image:: /Egon-Sketch.jpg

In the sketch, this is the node labeled "Raspi". A "generic"
component-based application that can be configured to act as ...

* ... a datalogger with various data sources and sinks. There are
  components available that read and write data from and to MQTT
  topics, for example. Likewise, CAN bus sources and sinks are
  available, and of course there are ways to read data from sensors
  connected locally on Linux.
* ... a control application with the usual set of sensors and actors.

A Simple Example
----------------

The following example application paints a sine wave on the
screen. Note that this is not a typical application because there are
less overengineered ways out there to paint sine waves - but you get
the point.  The application uses only two components,

* A mocked data source (:doc:`sourcedoc/mock-source`), configured to
  emit samples that form a sine wave
* A data sink that animates the samples on the screen.

.. literalinclude:: ../../Raspi/src/endless/conf/sine-plot.conf
   :caption: :download:`sine-plot.conf (download)
             <../../Raspi/src/endless/conf/sine-plot.conf>`
   :language: python

Running the plot:

.. code-block:: console

   $ run-components --configfile sine-plot.conf

A More Involved Example
-----------------------

.. toctree::
   :hidden:

   complicated-example/index
   satellite/index

See :doc:`complicated-example/index`

Source Code Documentation
-------------------------

.. toctree::
   :hidden:

   sourcedoc/index

See :doc:`sourcedoc/index`
