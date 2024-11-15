.. ot-group:: yocto

Todo List
=========

.. contents::
   :local:

``sshd`` Socket Activation
--------------------------

This would make boots a little faster. Look into
``poky/meta/recipes-connectivity/openssh/openssh_9.9p1.bb`` how this
is done (``PACKAGECONFIG``).

Different Images For Different Purposes
---------------------------------------

Status
......

In the works. 

* ``endless-image-base``
* ``endless-image-fulldev``, based upon ``endless-image-base``
* others to come

Examples
........

* ``development``. Debug info, SDK, development packages (headers and
  such).
* ``student``. One for each student, or one with all students. Or
    both. Inherits ``development``. SSH public keys included, ideally.
* ``endless_internal``. Password ``root1234``, of course. Inherits
    ``development``

Notes
.....

* See the ``extrausers.bbclass`` class
* https://docs.yoctoproject.org/ref-manual/features.html

Maximize Image At First Boot
----------------------------

Add systemd unit that enlarges rootfs to take available SD card space
(at first boot only, ideally)

.. code-block:: console

   $ parted /dev/mmcblk0 'resizepart 2 100%'
   $ resize2fs /dev/mmcblk0p2

Add User ``endless``
--------------------

Groups ``i2c``, ``gpio``, etc
