#pragma once

#include <string>


class Sensor
{
public:
    Sensor(const std::string& filename);
    double get_temperature() const;
private:
    const std::string _filename;
};

