Components, And All That
========================

.. contents::
   :local:

Overview: Components, Facets, Receptacles
-----------------------------------------

Components are objects that implement functionality. Access to that
funtionality is provided via stubs, so-called *facets*.

A component may use functionality of another component via its
facets. For this, you connect together both components by plugging one
component's facet into a compatible *receptacle* of the using
component.

jjj sketch of what follows

.. literalinclude:: ../../../Raspi/tests/test_connected_components.py
   :language: python


``Component`` Base Class
------------------------

.. autoclass:: endless.component.Component
   :members:

Defining Facets And Receptacles
-------------------------------

.. autoclass:: endless.facet.facet
   :members:

.. autoclass:: endless.receptacle.receptacle
   :members:

Running Components: Lifetime and Error Management
-------------------------------------------------

.. autoclass:: endless.component.LifetimeComponent
   :members:

.. autoclass:: endless.runner.Runner
   :members:

.. autoclass:: endless.errorhandler.ErrorHandler
   :members:

