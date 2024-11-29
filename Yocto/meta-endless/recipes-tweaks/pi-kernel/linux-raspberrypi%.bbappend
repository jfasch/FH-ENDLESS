# /dev/gpiomem is raspi specific. used by wiringpi and pigpio which
# are also raspi specific.

FILESEXTRAPATHS:prepend := "${THISDIR}/files:"
SRC_URI += "file://no-dev-gpiomem.cfg"


# export /dev/i2c-1 for userspace i2c

KERNEL_MODULE_AUTOLOAD += " i2c-dev"
