The ENDLESS Project
===================

See the `ReadTheDocs CI
<https://fh-endless.readthedocs.io/en/latest/>`__ if you intend to
*consume* documentation.

Developers, And Documentation
-----------------------------

If you are a developer, you probably want to build the documentation
locally and try it out before you commit/push. The documentation is
massaged into a pile of static HTML pages by the `Sphinx documentation
system <https://www.sphinx-doc.org/en/master/>`__; follow the steps
below.

.. * Install prerequisites through your distribution's package
..   management.  This is Fedorish; other distros like Debian/Ubuntu
..   *should* work, but might vary in their package names.
.. 
..   .. code-block:: console


* ``Documentation/requirements.txt`` contains a lot, it's probably
  best to use a virtual environment

  .. code-block:: console

     $ python -m venv ~/My-Environments/endless-documentation
     $ . ~/My-Environments/endless-documentation/bin/activate
     $ python -m pip install -r Documentation/requirements.txt

* ``chdir`` to ``Documentation/``, and build

  .. code-block:: console

     $ cd Documentation/
     $ make html
     ... roedel ...

* The build lands in ``/tmp/endless/``; point your browser to
  ``/tmp/endless/html/index.html``
