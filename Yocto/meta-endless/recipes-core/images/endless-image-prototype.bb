SUMMARY = "ENDLESS Image (Full Development Version + Prototype)"
LICENSE = "CLOSED"

require endless-image-fulldev.bb

IMAGE_INSTALL:append = " endless-prototype"
