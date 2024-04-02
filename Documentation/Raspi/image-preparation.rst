Preparing A Bootable Image
==========================

.. contents::
   :local:

Note that we will once switch to Yocto for image preparation; this is
considered preliminary.

Adding User ``endless``
-----------------------

For ages, the Pi OS came with user ``pi``, and a well-known password
``raspberry``. If SSH access is configured, that user can login from
the net. This has been recognized as a major security flaw (to put it
mildly), especially as Raspberries tend to be opened up to the
internet by inexperienced users. http://rptl.io/newuser explains the
security implications, and describes how to create a dedicated user on
a running Pi.

Booting a Pi to create a user is inadequate if we want to create
images automatically. Here's how to create a user in an image without
ever booting it [#useradd]_.

#. Create user's own primary group

   Add the following line to ``<rootfs-mountpoint>/etc/group``,

   .. code-block:: text

      endless:x:1500

#. Create user

   Add the following to ``<rootfs-mountpoint>/etc/passwd``

   .. code-block:: text

      endless:x:1500:1500:Endless User:/home/endless:/bin/bash

#. Add user to ``sudo`` group

   Modify the ``sudo`` group record to contain the ``endless`` user,

   .. code-block:: text

      sudo:x:27:pi,endless

#. Create home directory

   .. code-block:: console

      # mkdir <rootfs-mountpoint>/home/endless
      # chown 1500:1500 <rootfs-mountpoint>/home/endless

#. Create a password (the ``openssl`` package needs to be installed),

   .. code-block:: console
      
      $ echo 'the-end1e$$-pa$$w0rd' | openssl passwd -6 -stdin
      $6$dgYaCZyRr1ikyqTM$xdSxOKCHRSryOdVMs18vZMHEtfSlDv.KO3BJTfV7DSLdNz62M5JUW6hEUqhlm2uAu8IZKeio81sZDeG7u7byw0

   .. note::

      This is a proof of concept. If you want to be serious, choose
      another password :-)

   Add the following line to ``<rootfs-mountpoint>/etc/shadow``

   .. code-block:: text

      endless:$6$dgYaCZyRr1ikyqTM$xdSxOKCHRSryOdVMs18vZMHEtfSlDv.KO3BJTfV7DSLdNz62M5JUW6hEUqhlm2uAu8IZKeio81sZDeG7u7byw0:19734:0:99999:7:::

Starting SSH At Boot
--------------------

Create a file ``<rootfs-mountpoint>/ssh``.

.. rubric:: Footnotes
.. [#useradd] This instruction roughly mimics what the `useradd
              <https://man7.org/linux/man-pages/man8/useradd.8.html>`__
              command does.

Configure CAN Controller
------------------------

.. sidebar::

   See https://www.waveshare.com/wiki/RS485_CAN_HAT

In ``<bootfs-mountpoint>/firmware/config.txt``, add the following lines,

.. code-block:: text

   dtparam=spi=on
   dtoverlay=mcp2515-can0,oscillator=12000000,interrupt=25,spimaxfrequency=2000000
