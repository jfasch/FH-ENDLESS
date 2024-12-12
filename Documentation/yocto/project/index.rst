.. ot-group:: yocto

Todo List
=========

.. contents::
   :local:

Basic Fixes
-----------

``endless`` Recipes
-------------------

* User ``endless``

  * Add to groups ``i2c``, ``gpio``
  * Aliases
  * Password for user ``endless``
  * ``sudo`` rules for user ``endless``
  * Check sshd config (enable password auth, possibly)

* ``root`` -> nologin (base)
* I2C: currently i2c is only forced into kernel on pi. bring it to
  other kernels to ->
  poky/meta/classes-recipe/linux-kernel-base.bbclass maybe?
* I2C: likewise, ``KERNEL_MODULE_AUTOLOAD`` is only done in
  meta-endless/recipes-tweaks/pi-kernel/linux-raspberrypi%.bbappend. bring
  it to all kernels (and make sure we compile i2c-dev on all kernels)

  .. code-block:: plaintext

     # udevadm info /dev/i2c-*
     ...
     P: /devices/pci0000:00/0000:00:02.0/i2c-10/i2c-dev/i2c-10
     M: i2c-10
     R: 10
     U: i2c-dev
     D: c 89:10
     N: i2c-10
     L: 0
     E: DEVPATH=/devices/pci0000:00/0000:00:02.0/i2c-10/i2c-dev/i2c-10
     E: DEVNAME=/dev/i2c-10
     E: MAJOR=89
     E: MINOR=10
     E: SUBSYSTEM=i2c-dev
     ...


  ``meta-endless/recipes-core/admin/endless-accounts/files/endless-i2c.rules``

  .. code-block:: plaintext

     KERNEL=="i2c-*", GROUP="i2c", MODE="0660"

* udev rules

  * put in ``/usr/lib/udev/rules.d`` (preinstalled, not configured
    on-site)
  * assign ``/sys/class/gpio`` (and ``/dev/gpiochipXXX``?) to group
    ``gpio``

CI Tests: TFTP/NFS Boot
-----------------------

* Provide recipe(s) and a containing image for CI testing
* Kernel and root filesystem on endless server (which user?)
* Automatically boot SUT

Recipe: ``endless`` Demo Application
------------------------------------

You know, that Python thing: :doc:`/Raspi/index`

* meta-raspberrypi/recipes-devtools/python/rpi-gpio_0.7.1.bb: ``inherit pypi setuptools``
* Application (base recipe), including systemd unit file
* Config file recipe(s). Start with one "demo" config which is
  packaged in a "demo" image
* See `Packaging and installing own Python program for/on Yocto
  <https://stackoverflow.com/questions/76529171/packaging-and-installing-own-python-program-for-on-yocto>`__

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

Image Documentation
-------------------

* i2c and spi configured in /boot/config.txt
* sysfs GPIO number space 

  .. code-block:: console

     # echo 25 > /sys/class/gpio/export
     [...ts...] export_store: invalid GPIO 25
     write error: Invalid argument

  .. code-block:: console

     # cat /sysclass/gpio/gpiochip512/base
     512

  .. code-block:: console

     # echo $((512+25)) > /sys/class/gpio/export


