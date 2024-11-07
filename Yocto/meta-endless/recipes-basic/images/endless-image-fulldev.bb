require endless-image.bb

SUMMARY = "Prototype ENDLESS Image (Full Development Version)"
LICENSE = "GPLv3"

# https://docs.yoctoproject.org/ref-manual/features.html
DISTRO_FEATURES += " bluetooth systemd wifi usrmerge vfat"
MACHINE_FEATURES += " bluetooth vfat"
IMAGE_FEATURES += " dbg-pkgs dev-pkgs doc-pkgs"
