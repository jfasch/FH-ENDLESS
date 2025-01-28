DESCRIPTION = "An ENDLESS prototype application"
HOMEPAGE = "https://github.com/jfasch/FH-ENDLESS"
LICENSE = "CLOSED"

SRC_URI = "git://github.com/jfasch/FH-ENDLESS;protocol=https;branch=main"
SRCREV = "6385ff16d9204a08b98edb42f43b0ddbac7c9543"

S = "${WORKDIR}/git"
PEP517_SOURCE_PATH = "${S}/Raspi"

RDEPENDS:${PN} += " python3-aiomqtt"

inherit python_setuptools_build_meta

do_install:append() {
    install -d ${D}/etc/endless
    install -d ${D}/etc/systemd/system
    install -d ${D}/usr/lib/systemd/system
    mv ${D}/usr/lib/python3.12/site-packages/endless/conf/sine-to-mqtt.conf ${D}/etc/endless
    mv ${D}/usr/lib/python3.12/site-packages/endless/service/endless-sine-to-mqtt.service ${D}/usr/lib/systemd/system
    ln -s /usr/lib/systemd/system/endless-sine-to-mqtt.service ${D}/etc/systemd/system
}



FILES:${PN} += "/usr/lib/systemd /usr/lib/systemd/system /usr/lib/systemd/system/endless-sine-to-mqtt.service"
