.. ot-group:: project_management

Project Management
==================

* Create dependency graph

  * ``Source`` and ``Sink`` error handling. Define Logger task; look
    into ``logging``
  * ``MockSource``: parameterize values, just like timestamps
  * Think about timestamps. Currently these are milliseconds since an
    arbitrary startiong point. Probably should be a
    ``datetime.datetime``, once and for all.
