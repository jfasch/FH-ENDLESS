# enable sshd; see
# poky/meta/recipes-connectivity/openssh/openssh_9.9p1.bb 

PACKAGECONFIG += "systemd-sshd-service-mode"
