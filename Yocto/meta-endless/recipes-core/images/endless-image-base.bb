SUMMARY = "ENDLESS Image (Base Definition)"
LICENSE = "GPLv3"

inherit core-image

IMAGE_INSTALL:append = " python3"
IMAGE_INSTALL:append = " parted"
IMAGE_INSTALL:append = " e2fsprogs-resize2fs"

IMAGE_INSTALL:append = " endless-accounts"
