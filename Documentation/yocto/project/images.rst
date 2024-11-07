.. ot-task:: yocto.images

Different Images For Different Purposes
=======================================

.. contents::
   :local:

Examples
--------

* ``development``. Debug info, SDK, development packages (headers and
  such).
* ``student``. One for each student, or one with all students. Or
    both. Inherits ``development``. SSH public keys included, ideally.
* ``endless_internal``. Password ``root1234``, of course. Inherits
    ``development``

Notes
-----

* See the ``extrausers.bbclass`` class
* https://docs.yoctoproject.org/ref-manual/features.html

Management
----------

* Git release branches
* Image and SDK versioning based on the release branch name

  * https://git.yoctoproject.org/poky/tree/meta/recipes-core/os-release/os-release.bb

