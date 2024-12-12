SUMMARY = "ENDLESS Image (Full Development Version)"
LICENSE = "GPLv3"

require endless-image-base.bb

# login for devs
IMAGE_INSTALL:append = " openssh"

# better tools for devs
IMAGE_INSTALL:append = " bash"
IMAGE_INSTALL:append = " coreutils"
IMAGE_INSTALL:append = " findutils"
IMAGE_INSTALL:append = " procps"
IMAGE_INSTALL:append = " less"
IMAGE_INSTALL:append = " iproute2"

# user endless may become root (who cannot login)
IMAGE_INSTALL:append = " sudo"


IMAGE_FEATURES += " dev-pkgs doc-pkgs"
# dbg-pkgs    was that that reason why all goes to /usr/bin/.debug?
