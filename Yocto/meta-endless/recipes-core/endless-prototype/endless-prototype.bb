DESCRIPTION = "An ENDLESS prototype application"
HOMEPAGE = "https://github.com/jfasch/FH-ENDLESS"
LICENSE = "CLOSED"


SRC_URI = "git://github.com/jfasch/FH-ENDLESS;protocol=https;branch=main"
SRCREV = "0317fd85e04780f191ede169d2e59b384612f45b"

S = "${WORKDIR}/git"

SETUPTOOLS_SETUP_PATH = "${S}/Raspi"
