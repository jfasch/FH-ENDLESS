.. ot-task:: yocto.maximize_image

Maximize Image At First Boot
============================

.. contents::
   :local:

* Add systemd unit that enlarges rootfs to take available SD card
  space (at first boot only, ideally)

  .. code-block:: console
  
     $ parted /dev/mmcblk0 'resizepart 2 100%'
     $ resize2fs /dev/mmcblk0p2
