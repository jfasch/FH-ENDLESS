#include "can-bus.h"
#include "sensor.h"

#include <iostream>
#include <string>
#include <chrono>
#include <thread>
#include <cstdint>

using namespace std::chrono_literals;


int main(int argc, char** argv)
{
    if (argc != 4) {
        std::cerr << "Usage: " << argv[0] << " <SENSOR-FILE> <CAN-INTERFACE> <CAN-ID>" << std::endl;
        return 1;
    }

    Sensor sensor(argv[1]);
    CANBus can(argv[2]);
    int can_id = std::stoi(argv[3]);

    for (;;) {
        uint64_t temperature = sensor.get_temperature() * 1000;

        // NOTE that we don't care about endianness. the Python
        // counterpart will treat it as little endian.
        const void* payload = (const void*)&temperature; 
        can.write({can_id, payload, 8});

        std::this_thread::sleep_for(1s);
    }

    return 0;
}
