#include "can-bus.h" 

#include "error.h"

#include <cassert>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <sys/ioctl.h>
#include <net/if.h>
#include <linux/can.h>


CANBus::CANBus(const std::string& iface)
{
    _fd = socket(PF_CAN, SOCK_RAW, CAN_RAW);
    if (_fd == -1)
        throw OSError(errno, "gosh: not getting a CAN socket from kernel?");

    struct ifreq ifr;
    strcpy(ifr.ifr_name, iface.c_str());
    int error = ioctl(_fd, SIOCGIFINDEX, &ifr);
    if (error == -1)
        throw OSError(errno, std::string("bad CAN interface name: \"") + iface + "\"");

    struct sockaddr_can addr;
    addr.can_family = AF_CAN;
    addr.can_ifindex = ifr.ifr_ifindex;

    error = bind(_fd, (struct sockaddr *)&addr, sizeof(addr));
    if (error == -1)
        throw OSError(errno, std::string("cannot bind CAN socket to interface \"") + iface + "\"");
}

CANBus::~CANBus()
{
    if (_fd != -1)
        close(_fd);
}

void CANBus::write(const Frame& f)
{
    can_frame cf;
    cf.can_id = f.id;
    cf.can_dlc = f.size;
    memcpy(cf.data, f.payload, f.size);

    ssize_t nwritten = ::write(_fd, &cf, sizeof(cf));
    if (nwritten == -1)
        throw OSError(errno, "cannot write CAN frame");

    assert(nwritten == sizeof(cf));  // can this happen?
}
