.. ot-group:: project_management

Project Management
==================

* Create dependency graph

  * ``Source`` and ``Sink`` error handling

    * Define Logger task; look into ``logging``
    * Define project's own exception base class, etc.

  * ``MockSource``: parameterize values, just like timestamps
  * Think about timestamps. Currently these are milliseconds since an
    arbitrary startiong point. Probably should be a
    ``datetime.datetime``, once and for all.
  * Arbitrary ``Sample`` structure. Add shape verification as members
    of data pipelines.
  * :doc:`../misc-notes/influxdb`
