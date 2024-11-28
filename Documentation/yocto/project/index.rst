.. ot-group:: yocto

Todo List
=========

.. contents::
   :local:

``endless`` Recipes
-------------------

* ``root`` -> nologin
* User ``endless``

  * Groups ``i2c``, ``gpio``, etc

* Dev addons for ``endless`` development

  * Password for user ``endless``
  * ``sudo`` rules for user ``endless``
  * Check sshd config (enable password auth, possibly)

Pi: Maximize Image At First Boot
--------------------------------

Add systemd unit that enlarges rootfs to take available SD card space
(at first boot only, ideally)

.. code-block:: console

   $ parted /dev/mmcblk0 'resizepart 2 100%'
   $ resize2fs /dev/mmcblk0p2

