#pragma once

#include <string>
#include <exception>


class OSError : public std::exception
{
public:
    OSError(int error /*errno*/, const std::string& prefix);
    virtual const char* what() const noexcept;
private:
    std::string _msg;
};

class SensorError : public std::exception
{
public:
    SensorError(const std::string& msg);
    virtual const char* what() const noexcept;
private:
    std::string _msg;
};
