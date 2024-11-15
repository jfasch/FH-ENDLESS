SUMMARY = "ENDLESS Image (Full Development Version)"
LICENSE = "GPLv3"

require endless-image-base.bb

IMAGE_INSTALL:append = " openssh"

IMAGE_FEATURES += " dev-pkgs doc-pkgs"
# dbg-pkgs    was that that reason why all goes to /usr/bin/.debug?
