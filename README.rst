The ENDLESS Project
===================

See `the docs CI on readthedocs
<https://fh-endless.readthedocs.io/en/latest/>`__ for the latest
documentation build.

Building Documentation Locally
------------------------------

* ``requirements.txt`` contains a lot, it's probably best to use a
  virtual environment

  .. code-block:: console

     $ python -m venv ~/My-Environments/endless
     $ . ~/My-Environments/endless/bin/activate
     $ python -m pip install -r requirements.txt

* ``chdir`` to ``Documentation/``, and build

  .. code-block:: console

     $ cd Documentation/
     $ make html
     ... roedel ...

* The build lands in ``/tmp/endless/``; point your browser to
  ``/tmp/endless/html/index.html``
