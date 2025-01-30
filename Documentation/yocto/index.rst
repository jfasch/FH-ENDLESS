.. include:: <mmlalias.txt>


Yocto: Building Linux OS Images
===============================

.. toctree::
   :hidden:

   project/index

.. toctree::

   image-preparation-fixme

.. todo::

   Absorb image-preparation-fixme into this document

.. contents::
   :local:

Work Environment (ENDLESS)
--------------------------

.. sidebar:: See also

   * :doc:`jfasch:trainings/material/soup/linux/ssh/group`.

.. code-block:: console

   $ ENDLESS_SERVER=ddd.ddd.ddd.ddd

Interactive Login On ``$ENDLESS_SERVER``
........................................

Required: an SSH account, setup by :doc:`the administrator
<jfasch:about/myself/index>`). My (``jfasch``'s) steps to setup my
daily work environment follow. It's all SSH, after all.

.. code-block:: console

   $ ssh jfasch@$ENDLESS_SERVER

Mounting And Unmounting My Home On ``$ENDLESS_SERVER``
......................................................

.. sidebar:: See also

   * :doc:`jfasch:trainings/material/soup/linux/ssh/sshfs`

.. code-block:: console

   $ mkdir ~/mounts/$ENDLESS_SERVER
   $ sshfs -o idmap=user -o uid=$(id -u) -o gid=$(id -g) $ENDLESS_SERVER: ~/mounts/$ENDLESS_SERVER

.. code-block:: console

   $ umount ~/mounts/$ENDLESS_SERVER

Yocto Development
-----------------

Work directory is the ``Yocto/`` subdirectory of the ``FH-ENDLESS`` project.

As of 2024-11-27, there are these build directories available:

* ``qemuarm64``
* ``qemux86-64``
* ``raspberry3-build``

QEMU (``MACHINE = qemux86-64``)
...............................

Setup Environment
`````````````````

.. code-block:: console

   $ . ~/FH-ENDLESS/Yocto/poky/oe-init-build-env ~/FH-ENDLESS/Yocto/qemux86-64/
   $ pwd
   /home/jfasch/FH-ENDLESS/Yocto/qemux86-64

Build An Image (``endless-image-fulldev``)
``````````````````````````````````````````

.. code-block:: console

   $ bitbake endless-image-fulldev

Test
````

Start QEMU on it. The ``slirp`` option did the trick, *everything just
works*.

.. code-block:: console

   $ runqemu nographic slirp

QEMU uses ``screen`` (or was it ``tmux``?) to capture the
terminal. ``C-a x`` is used to quit the session, and get back to the
shell where you started.

SSH Login
`````````

.. code-block:: console

   $ ssh -p 2222 endless@localhost

Raspberry Pi 3 (``MACHINE = raspberrypi3-64``)
..............................................

Setup Environment
`````````````````

.. code-block:: console

   $ . ~/FH-ENDLESS/Yocto/poky/oe-init-build-env ~/FH-ENDLESS/Yocto/raspberry3-build/
   $ pwd
   /home/jfasch/FH-ENDLESS/Yocto/raspberry3-build

Build An Image (``endless-image-fulldev``)
``````````````````````````````````````````

.. code-block:: console

   $ bitbake endless-image-fulldev

Test
````

Bring the generated ``.wic`` image onto the SD card.

The image file (see
https://docs.yoctoproject.org/dev-manual/wic.html)

.. code-block:: console

   $ ls -l tmp/deploy/images/raspberrypi3-64/endless-image-fulldev-raspberrypi3-64.rootfs.wic.bz2
   lrwxrwxrwx 2 jfasch jfasch 67 Nov 27 13:29 tmp/deploy/images/raspberrypi3-64/endless-image-fulldev-raspberrypi3-64.rootfs.wic.bz2 -> endless-image-fulldev-raspberrypi3-64.rootfs-20241127121726.wic.bz2

Uncompress

.. code-block:: console

   $ bzip -cd tmp/deploy/images/raspberrypi3-64/endless-image-fulldev-raspberrypi3-64.rootfs.wic.bz2 > uncompressed-image.wic
   $ sudo cp uncompressed-image.wic /dev/mmcblk0

Over SSH on the fly directly onto the SD card that is in my laptop's
SD slot,

.. code-block:: console

   $ ssh $ENDLESS_SERVER \
        'bzip2 -cd /home/jfasch/FH-ENDLESS/Yocto/raspberry3-build/tmp/deploy/images/raspberrypi3-64/endless-image-fulldev-raspberrypi3-64.rootfs.wic.bz2' \
        | sudo sh -c 'cat > /dev/mmcblk0'

A Collection Of Commandlines
............................

* Find out which package provides a file

  .. code-block:: console

     $ oe-pkgdata-util find-path /usr/share/man/man1/groups.1
     shadow-doc: /usr/share/man/man1/groups.1

Kernel Config Fragments
.......................

https://wiki.koansoftware.com/index.php/Modify_the_linux_kernel_with_configuration_fragments_in_Yocto

Project Management
------------------

* :doc:`project/index`

To Be Cleaned
-------------

Basic Information
.................

* https://docs.yoctoproject.org/brief-yoctoprojectqs/index.html
* https://docs.yoctoproject.org/dunfell/what-i-wish-id-known.html
* https://docs.yoctoproject.org/ref-manual/system-requirements.html#fedora-packages

  .. code-block:: console

     $ sudo dnf install gawk make wget tar bzip2 gzip python3 unzip perl patch diffutils diffstat git cpp gcc gcc-c++ glibc-devel texinfo chrpath ccache perl-Data-Dumper perl-Text-ParseWords perl-Thread-Queue perl-bignum socat python3-pexpect findutils which file cpio python python3-pip xz python3-GitPython python3-jinja2 rpcgen perl-FindBin perl-File-Compare perl-File-Copy perl-locale zstd lz4 hostname glibc-langpack-en libacl

* Releases: https://wiki.yoctoproject.org/wiki/Releases

  |longrightarrow| ``scarthgap`` (latest LTS)

Raspberry Build
...............

.. sidebar::

   * `meta-raspberrypi
     <https://github.com/agherzan/meta-raspberrypi>`__

Project Setup
`````````````

* Change into ``~/My-Projects/yocto``
* use ``poky@HEAD``

  .. code-block:: console

     $ git clone https://git.yoctoproject.org/poky

* Create ``raspberrypi3-64`` build directory

  .. code-block:: console

     $ pwd
     ~/My-Projects/yocto
     $ . poky/oe-init-build-env raspberrypi3-64
     ... blah ...
     $ pwd
     ~/My-Projects/yocto/raspberrypi3-64

* Set machine type that we build for

  In ``~/My-Projects/yocto/raspberry3-build/conf/local.conf``, add the
  following line

  .. code-block:: console
 
     MACHINE = "raspberrypi3-64"

* Get ``meta-raspberrypi``

  .. code-block:: console

     $ cd ~/My-Projects/yocto
     $ git clone https://github.com/agherzan/meta-raspberrypi

* Add ``meta-raspberrypi`` to layers

  In ``~/My-Projects/yocto/raspberry3-build/conf/bblayers.conf``, add

  .. code-block:: console

     BBLAYERS += " ${HOME}/My-Projects/yocto/meta-raspberrypi"

* Share download and sstate directories (for repeated builds, and in
  case we want to build for a Pi4)

  In ``~/My-Projects/yocto/raspberry3-build/conf/local.conf``, add the
  following lines

  .. code-block:: console

     DL_DIR = "${HOME}/My-Projects/yocto/DOWNLOAD
     SSTATE_DIR = "${HOME}/My-Projects/yocto/SSTATE"
