DESCRIPTION = "Enlarge Pi's RootFS at first boot"
LICENSE = "CLOSED"

S = "${WORKDIR}/sources"
UNPACKDIR = "${S}"

inherit systemd

SYSTEMD_AUTO_ENABLE:${PN} = "enable"
SYSTEMD_SERVICE:${PN} = "pi-enlarge-rootfs.service"

SRC_URI = "\
	file://pi-enlarge-rootfs \
	file://pi-enlarge-rootfs.service \
	"

do_install() {
	install -d -m 755 ${D}/usr/libexec/endless
	install -m 755 pi-enlarge-rootfs ${D}/usr/libexec/endless

	install -d -m 755 ${D}/usr/lib/systemd/system
	install -m 644 pi-enlarge-rootfs.service ${D}/usr/lib/systemd/system

 	install -d -m 755 ${D}/var/lib/endless
}

FILES:${PN} = "\
	/usr/libexec/endless/pi-enlarge-rootfs \	
 	/usr/lib/systemd/system/pi-enlarge-rootfs.service \
	/var/lib/endless \
"
