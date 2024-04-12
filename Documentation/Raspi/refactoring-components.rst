Refactoring to Components
=========================

.. contents::
   :local:

Goal
----

Goal is to eliminate the concept of ``Source`` and ``Sink``. They are
both very similar in their startup and sutdown behavior, and offer
very little in the way of adding unrelated functionality like
controlling actors.

Components
----------

Components *provide* (i.e. are-not-inherited-from) interfaces they
happen to have, such as ...

* *Lifetime*. Components that act as datasources (MQTT for example)
  typically employ an internal task to react upon incoming data. Other
  (filters for example) will not.
* *Data Outlets*. An ex ``Source`` component has a data outlet that
  has to be connected to another, *consumer* type interface of another
  component.

Todo
----

* ``Runner`` continues when an ENDLESS exception is seen, else
  terminates
* ``Lifetime.stop()``: shouldn't it await task?
* Put the tiresome ``await asyncio.sleep(0)`` (currently in
  ``Outlet``) into the right place, whatever that place is.
* Implement ``Runner`` as ``@contextlib.asynccontextmanager``. Raise
  ``TerminationRequest`` instead of calling ``runner.stop()``
* Implement ``errorhandler.ErrorReporter`` as
  ``@contextlib.asynccontextmanager``. Is there a test for it?
* ``Sample`` should carry a ``tag``, not a ``name``
* ``MQTT``: make tag-to-topic mapping more intelligent. Respectively,
  pull out MQTT client object and re-use it in multiple MQTT sinks,
  with a mapping component that distributes samples by their tags.
