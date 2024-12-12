DESCRIPTION = "Create 'endless' user, and fiddle with groups"
# HOMEPAGE = ""
LICENSE = "CLOSED"

# notes
# -----

# * I'd like to inhibit root login here in this file, to have
#   everything central. this is not possible with 'inherit useradd'
#   though, so I have to 'inherit extrausers` in the image recipe
#   ('extrausers' can only be used from image recipes).

SRC_URI = "\
	file://.bashrc \
	file://endless-i2c.rules \
	file://sudoers-sudo-group \
	"

S = "${WORKDIR}/sources"
UNPACKDIR = "${S}"

DEPENDS_${PN} += " sudo-lib"

inherit useradd

# create user password "endless" on host, and add outcome to
# USERADD_PARAM:
# printf "%q" $(mkpasswd -m sha256crypt endless)
endless_passwd = "\$5\$OXJaECO8TL6F.UCk\$kUjHX2nsRlmNiVsb3R2q9VTZexWhO5HgnzVilb8Ezj7"

USERADD_PACKAGES = "${PN}"
USERADD_PARAM:${PN} = "--uid 4711 --gid endless --groups i2c,sudo --password '${endless_passwd}' --home-dir /home/endless --create-home --shell /bin/bash endless"
GROUPADD_PARAM:${PN} = "--gid 4711 endless;i2c"

do_install () {
    install -d -m 700 ${D}/home/endless
    install -p -m 600 .bashrc ${D}/home/endless
    chown -R endless ${D}/home/endless/

    install -d -m 755 ${D}/usr/lib/udev/rules.d
    install -m 644 endless-i2c.rules ${D}/usr/lib/udev/rules.d

    install -d -m 750 ${D}/etc/sudoers.d
    install -m 600 sudoers-sudo-group ${D}/etc/sudoers.d
}

FILES:${PN} = "\
    /home/endless/.bashrc \
    /usr/lib/udev/rules.d/endless-i2c.rules \
    /etc/sudoers.d/sudoers-sudo-group \
"
