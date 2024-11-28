.. ot-group:: yocto

Todo List
=========

.. contents::
   :local:

``endless`` Development Recipes
-------------------------------

* ``root`` -> nologin
* User ``endless``

  * Groups ``i2c``, ``gpio``, etc

* Dev addons for ``endless`` development

  * Password for user ``endless``
  * ``sudo`` rules for user ``endless``
  * Check sshd config (enable password auth, possibly)

CI Tests: TFTP/NFS Boot
-----------------------

* Provide recipe(s) and a containing image for CI testing
* Kernel and root filesystem on endless server (which user?)
* Automatically boot SUT

Recipe: ``endless`` Demo Application
------------------------------------

You know, that Python thing: :doc:`/Raspi/index`

* Application (base recipe), including systemd unit file
* Config file recipe(s). Start with one "demo" config which is
  packaged in a "demo" image

Recipe: Crazy Car (Future)
--------------------------

* https://fh-stece2022.readthedocs.io/en/latest/index.html
* Accounts for students

Pi: Maximize Image At First Boot
--------------------------------

Add systemd unit that enlarges rootfs to take available SD card space
(at first boot only, ideally)

.. code-block:: console

   $ parted /dev/mmcblk0 'resizepart 2 100%'
   $ resize2fs /dev/mmcblk0p2

