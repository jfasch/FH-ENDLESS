#include "error.h"

#include <string>
#include <string.h>


OSError::OSError(int error /*errno*/, const std::string& prefix)
: _msg(prefix)
{
    char buf[64];
    strerror_r(error, buf, sizeof(buf));
    _msg += " (";
    _msg += std::to_string(error);
    _msg += "/\"";
    _msg += buf;
    _msg += "\")";
}

const char* OSError::what() const noexcept
{
    return _msg.c_str();
}

SensorError::SensorError(const std::string& msg)
: _msg(msg) {}

const char* SensorError::what() const noexcept
{
    return _msg.c_str();
}
