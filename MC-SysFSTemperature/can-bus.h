#pragma once

#include <string>


class CANBus
{
public:
    struct Frame
    {
        int id;
        const void* payload;
        unsigned size;
    };

public:
    CANBus(const std::string& iface);
    ~CANBus();

    void write(const Frame&);

private:
    int _fd = -1;
};

