.. include:: <mmlalias.txt>


Yocto: Building Linux OS Images
===============================

.. contents::
   :depth: 1
   :local:

Yocto Development And Build
---------------------------

Getting
.......

.. sidebar:: Git Repo

   * https://github.com/jfasch/FH-ENDLESS

.. code-block:: console

   $ git clone https://github.com/jfasch/FH-ENDLESS
   $ git submodule init
   Submodule 'Yocto/meta-raspberrypi' (https://github.com/agherzan/meta-raspberrypi) registered for path 'Yocto/meta-raspberrypi'
   Submodule 'Yocto/poky' (https://git.yoctoproject.org/poky) registered for path 'Yocto/poky'

.. code-block:: console

   $ git submodule update
   Cloning into '/home/jfasch/My-Projects/FH-ENDLESS-nici/Yocto/meta-raspberrypi'...
   Cloning into '/home/jfasch/My-Projects/FH-ENDLESS-nici/Yocto/poky'...
   Submodule path 'Yocto/meta-raspberrypi': checked out 'd5ffe135c73ab940148e595c6fb010d50ddcfc60'
   Submodule path 'Yocto/poky': checked out 'a6c1af1af5baad083f0c98acd9957ccabdd49067'

Structure
.........

The ``FH-ENDLESS`` project contains not only the Yocto build. For
Yocto, go to the ``Yocto/`` subdirectory.

``poky/`` (Submodule)
`````````````````````

.. sidebar:: Git Repo

   * https://git.yoctoproject.org/poky

``poky/`` contains the upstream ``https://git.yoctoproject.org/poky``
sources - the Yocto core, so to say (Yocto has a long history, and
it's not always clear what the relationship between OpenEmbedded and
Poky is).

``meta-raspberrypi/`` (Submodule)
`````````````````````````````````

.. sidebar:: Git Repo

   * https://github.com/agherzan/meta-raspberrypi

This is the BSP layer for the raspberry build (see below).

Build Directories
`````````````````

As of 2024-11-27, there are the following build directories available:

* ``qemuarm64/``
* ``qemux86-64/``
* ``raspberry3-build/``

.. sidebar:: Config files

   * `Yocto/common-local.conf
     <https://github.com/jfasch/FH-ENDLESS/blob/main/Yocto/common-local.conf>`__
   * `Yocto/common-bblayers.conf
     <https://github.com/jfasch/FH-ENDLESS/blob/main/Yocto/common-bblayers.conf>`__

Each of those contains a ``conf/`` subdirectory with two config files,
``conf/local.conf`` and ``conf/bblayers.conf``. To avoid duplication
of setting, these files delegate (include) common settings from the
files ``common-local.conf`` and ``common-bblayers.conf`` in the
toplevel ``Yocto/`` directory.

Building
........

Best to start with the Qemu variant because it is more easily tested
than the Raspi variants.

When you run ``bitbake`` the first time, you migt encounter errors
like

.. code-block:: console

   $ bitbake endless-image-fulldev
   ERROR: The following required tools (as specified by HOSTTOOLS) appear to be unavailable in PATH, please install them in order to proceed:
     chrpath diffstat lz4c patch rpcgen

Install the tools using your distribution's package manager [#fedora]_

QEMU (``MACHINE = qemux86-64``)
```````````````````````````````

Setup Environment
'''''''''''''''''

.. code-block:: console

   $ . ~/FH-ENDLESS/Yocto/poky/oe-init-build-env ~/FH-ENDLESS/Yocto/qemux86-64/
   $ pwd
   /home/jfasch/FH-ENDLESS/Yocto/qemux86-64

Build An Image (``endless-image-fulldev``)
''''''''''''''''''''''''''''''''''''''''''

.. code-block:: console

   $ bitbake endless-image-fulldev

Test
''''

Start QEMU on it. The ``slirp`` option did the trick, *everything just
works*.

.. code-block:: console

   $ runqemu nographic slirp

QEMU uses ``screen`` (or was it ``tmux``?) to capture the
terminal. ``C-a x`` is used to quit the session, and get back to the
shell where you started.

SSH Login
'''''''''

.. code-block:: console

   $ ssh -p 2222 endless@localhost

Raspberry Pi 3 (``MACHINE = raspberrypi3-64``)
``````````````````````````````````````````````

Setup Environment
'''''''''''''''''

.. code-block:: console

   $ . ~/FH-ENDLESS/Yocto/poky/oe-init-build-env ~/FH-ENDLESS/Yocto/raspberry3-build/
   $ pwd
   /home/jfasch/FH-ENDLESS/Yocto/raspberry3-build

Build An Image (``endless-image-fulldev``)
''''''''''''''''''''''''''''''''''''''''''

.. code-block:: console

   $ bitbake endless-image-fulldev

Test
''''

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

Work Environment Preparation (On ENDLESS Server Machine)
--------------------------------------------------------

Yocto can be built purely locally, on your own laptop. It might take a
while though, and you'd have to make sure that the CPU is well
ventilated.

This section describes a way to use a dedicated build server:

* SSH for interactive remote login, to run Yocto's build commands
* SSH to mount the remote Yocto tree locally, so I can use a local
  text editor for development

.. sidebar:: See also

   * :doc:`jfasch:trainings/material/soup/linux/ssh/index`.

The address of the remote build server is used by several commands
described below; we store it in a variable that we reference below.

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

Use the ``sshfs`` command to mount the remote user's home directory
locally under ``~/mounts/$ENDLESS_SERVER``. We use the ``idmap`` mount
option because the local user's UID/GID might not match the remote
user's.

.. code-block:: console

   $ mkdir ~/mounts/$ENDLESS_SERVER
   $ sshfs -o idmap=user -o uid=$(id -u) -o gid=$(id -g) $ENDLESS_SERVER: ~/mounts/$ENDLESS_SERVER

.. code-block:: console

   $ umount ~/mounts/$ENDLESS_SERVER

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

Links
.....

* https://docs.yoctoproject.org/brief-yoctoprojectqs/index.html
* https://docs.yoctoproject.org/dunfell/what-i-wish-id-known.html
* https://docs.yoctoproject.org/ref-manual/system-requirements.html#fedora-packages
* Releases: https://wiki.yoctoproject.org/wiki/Releases

  |longrightarrow| ``scarthgap`` (latest LTS)

Future Directions
-----------------

.. toctree::
   :maxdepth: 1

   project/index

Random/Half-Obsolete Notes
--------------------------

.. toctree::
   :hidden:

   image-preparation-fixme

* Some pre :doc:`Yocto notes on how to tune a Raspberry OS
  installation <image-preparation-fixme>`

.. rubric:: Footnotes
.. [#fedora] On Fedora 42 (which is not yet supported/tested by Yocto
             upstream) for example, I had to say

	     .. code-block:: console

		$ sudo dnf install chrpath diffstat lz4 patch rpcgen
		$ sudo dnf install perl-FindBin perl-STD
