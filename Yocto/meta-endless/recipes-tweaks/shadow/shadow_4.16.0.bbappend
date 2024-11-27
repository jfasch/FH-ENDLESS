# fix shadow's missing respect from alternative providers of
# man1/groups.1

ALTERNATIVE:${PN}-doc += " groups.1"
ALTERNATIVE_LINK_NAME[groups.1] = "${mandir}/man1/groups.1"

# image creation error when adding coreutils
# ------------------------------------------

# + update-alternatives --install /usr/share/man/man1/groups.1 groups.1 /usr/share/man/man1/groups.1.coreutils 100
# update-alternatives: Error: not linking /home/jfasch/FH-ENDLESS/Yocto/qemux86-64/tmp/work/qemux86_64-poky-linux/endless-image-fulldev/1.0/rootfs/usr/share/man/man1/groups.1 to /usr/share/man
# /man1/groups.1.coreutils since /home/jfasch/FH-ENDLESS/Yocto/qemux86-64/tmp/work/qemux86_64-poky-linux/endless-image-fulldev/1.0/rootfs/usr/share/man/man1/groups.1 exists and is not a link
# %post(coreutils-doc-9.5-r0.core2_64): waitpid(4090172) rc 4090172 status 100
# warning: %post(coreutils-doc-9.5-r0.core2_64) scriptlet failed, exit status 1
