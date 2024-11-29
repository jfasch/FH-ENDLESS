DESCRIPTION = "Create 'endless' user, and fiddle with groups"
# HOMEPAGE = ""
LICENSE = "CLOSED"
# SECTION = ""

# depend on i2c, gpio, etc set up (incl. udev rules for /sys/class)
# DEPENDS = ""
# LIC_FILES_CHKSUM = ""

SRC_URI = "file://.bashrc"

S = "${WORKDIR}/sources"
UNPACKDIR = "${S}"

inherit useradd

do_install () {
    # USERADD_PARAM ... --create-home does not create home. workaround
    # that.
    install -d -m 700 ${D}/home/endless
    install -p -m 600 .bashrc ${D}/home/endless
    chown -R endless ${D}/home/endless/
}

USERADD_PACKAGES = "${PN}"
USERADD_PARAM:${PN} = "--uid 4711 --gid endless --home-dir /home/endless --create-home --shell /bin/bash endless"
GROUPADD_PARAM:${PN} = "--gid 4711 endless"

FILES:${PN} = "/home/endless/.bashrc"




# root@qemux86-64:~# groupadd i2c 
# root@qemux86-64:~# groupadd gpio
# 
# 
# user endless
# 
# on host:
# printf "%q" $(mkpasswd -m sha256crypt endless)
# \$5\$IaDG0ZRukyPWfzWo\$moge.JIY2DiUc2H8flz/dTDohyPWTyDf.qnrrR3ozw9
# 
# install homedir (/home/endless) from files/
# 
# useradd --password ... 
# 
# 
# 
# inherit extrausers
# 
# EXTRA_USERS_PARAMS = " useradd customUser1; \
#                        useradd customUser2; \
#                        usermod  -p 'Password_1' customUser1; \
#                        usermod  -p 'Password_2' customUser2; \
#                        usermod  -a -G sudo customUser1; \
#                        usermod  -a -G sudo customUser2;"
