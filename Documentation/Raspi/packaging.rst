Packaging
=========

Test Packaging During Development: *Editable Install*
-----------------------------------------------------

* Setup virtual environment for package testing
  (:doc:`jfasch:trainings/material/soup/python/swdev/venv/screenplay`)

  .. code-block:: console

     $ python -m venv ~/My-Environments/endless-prototype-test
     ... roedel ...

* Activate environment

  .. code-block:: console

     $ . ~/My-Environments/endless-prototype-test/bin/activate
     (endless-prototype-test) $               # <-- prompt modified

* Install the package into ``endless-prototype-test``, as an *editable
  install*. This does not actually create a wheel file, but rather
  links into the source tree directly. Cool, because now you can
  continue developing/fixing in the source tree, and at the same time
  use the package as if you were one of its users. See
  https://setuptools.pypa.io/en/latest/userguide/development_mode.html.

  .. code-block:: console

     (endless-prototype-test) $ python -m pip install --editable ~/My-Projects/FH-ENDLESS/Raspi/

Finally: Create Package From Source
-----------------------------------

.. sidebar:: See also

   * https://packaging.python.org/en/latest/flow/

Build Wheel File
................

.. code-block:: console

   $ pwd
   /home/jfasch/My-Projects/FH-ENDLESS/Raspi
   $ python3 -m build --wheel

.. code-block:: console

   $ ls -l dist/
   total 24
   -rw-r--r--. 1 jfasch jfasch 20698 Jan 14 10:26 endless_prototype-0.1.0-py3-none-any.whl

What's In A Wheel
.................

.. code-block:: console

   $ unzip -l dist/endless_prototype-0.1.0-py3-none-any.whl 
   Archive:  dist/endless_prototype-0.1.0-py3-none-any.whl
     Length      Date    Time    Name
   ---------  ---------- -----   ----
           0  12-16-2024 14:21   endless/__init__.py
           0  12-16-2024 14:21   endless/framework/__init__.py
         580  05-02-2024 08:48   endless/framework/async_util.py
         841  06-07-2024 07:54   endless/framework/can_reader.py
   ...

Packaging Details
-----------------

Data Files
..........

End goal is that the ``endless-prototype`` package installation brings
e.g. ``sample.conf`` (to be used by ``run-conponents``) into
``/etc/endless/``. **This is not easy!**

The preferred Python packaging way nowadays is to write packaging
information in ``pyproject.toml``; ``setup.py`` and ``setup.cfg`` is
long deprecated. Platform dependencies (like installing data files
into ``/etc/endless/``, for example) are deprecated - "that's the
responsibility of package managers", they say.

This discussion makes matters clear, especially Michał Górny's answer:
https://discuss.python.org/t/best-practice-for-documentation-its-installation/25159/3

*Solution*

* Cram data files into ``site-packages/endless``, where the Python
  files are.
* Let the Yocto recipe then sort it all out; for example

  * Move ``site-packages/endless/sine-plot.conf`` to ``/etc/endless/``
  * Move ``site-packages/endless/sine-plot.service`` to
    ``/etc/systemd/system/``

Links
-----

* https://packaging.python.org/en/latest/
* https://packaging.python.org/en/latest/flow/
* https://packaging.python.org/en/latest/tutorials/installing-packages/
