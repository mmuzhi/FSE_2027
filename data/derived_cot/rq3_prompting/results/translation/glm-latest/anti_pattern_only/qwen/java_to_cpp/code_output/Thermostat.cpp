#include <string>
#include <utility>

namespace org::example {

class Thermostat {
public:
    double currentTemperature;

    Thermostat(double currentTemperature, double targetTemperature, std::string mode)
        : currentTemperature(currentTemperature),
          targetTemperature(targetTemperature),
          mode(std::move(mode)) {}

    double getTargetTemperature() const {
        return targetTemperature;
    }

    void setTargetTemperature(double temperature) {
        this->targetTemperature = temperature;
    }

    std::string getMode() const {
        return mode;
    }

    bool setMode(std::string mode) {
        if (mode == "heat" || mode == "cool") {
            this->mode = std::move(mode);
            return true;
        } else {
            return false;
        }
    }

    void autoSetMode() {
        if (currentTemperature < targetTemperature) {
            this->mode = "heat";
        } else {
            this->mode = "cool";
        }
    }

    bool autoCheckConflict() {
        if (currentTemperature > targetTemperature) {
            if (mode == "cool") {
                return true;
            } else {
                autoSetMode();
                return false;
            }
        } else {
            if (mode == "heat") {
                return true;
            } else {
                autoSetMode();
                return false;
            }
        }
    }

    int simulateOperation() {
        autoSetMode();
        int useTime = 0;
        if (mode == "heat") {
            while (currentTemperature < targetTemperature) {
                currentTemperature += 1;
                useTime += 1;
            }
        } else {
            while (currentTemperature > targetTemperature) {
                currentTemperature -= 1;
                useTime += 1;
            }
        }
        return useTime;
    }

private:
    double targetTemperature;
    std::string mode;
};

} // namespace org::example