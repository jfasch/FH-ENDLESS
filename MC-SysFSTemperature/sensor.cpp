#include "sensor.h"

#include "error.h"

#include <stdexcept>
#include <string>

#include <fcntl.h>
#include <unistd.h>
#include <string.h>


Sensor::Sensor(const std::string& filename)
: _filename(filename) {}

double Sensor::get_temperature() const
{
    int fd = open(_filename.c_str(), O_RDONLY);
    if (fd == -1)
        throw OSError(errno, std::string("Cannot open sensor file " + _filename + " for reading"));

    char buffer[64];
    memset(buffer, 0, sizeof(buffer));
    ssize_t nread = read(fd, buffer, sizeof(buffer)-1);
    if (nread == -1) {
        close(fd);
        throw OSError(errno, std::string("Cannot read from sensor file ") + _filename);
    }

    close(fd);

    try {
        return std::stod(buffer);
    }
    catch (const std::invalid_argument&) {
        std::string msg = "Bad string read from sensor file ";
        msg += _filename;
        msg += ": \"";
        msg += buffer;
        msg += '\"';
        throw SensorError(msg);
    }
}
