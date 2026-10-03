#include <string>

class Thermostat {
private:
    double current_temperature;
    double target_temperature;
    std::string mode;

public:
    Thermostat(double current_temperature, double target_temperature, const std::string& mode) 
        : current_temperature(current_temperature), target_temperature(target_temperature), mode(mode) {}

    double get_target_temperature() const {
        return target_temperature;
    }

    void set_target_temperature(double temperature) {
        target_temperature = temperature;
    }

    std::string get_mode() const {
        return mode;
    }

    bool set_mode(const std::string& mode) {
        if (mode == "heat" || mode == "cool") {
            this->mode = mode;
            return true;
        }
        return false;
    }

    void auto_set_mode() {
        if (current_temperature < target_temperature) {
            mode = "heat";
        } else {
            mode = "cool";
        }
    }

    bool auto_check_conflict() {
        if (current_temperature > target_temperature) {
            if (mode == "cool") {
                return true;
            } else {
                auto_set_mode();
                return false;
            }
        } else if (current_temperature < target_temperature) {
            if (mode == "heat") {
                return true;
            } else {
                auto_set_mode();
                return false;
            }
        } else {
            // current temperature equals target temperature
            if (mode == "heat" || mode == "cool") {
                return true;
            } else {
                auto_set_mode();
                return false;
            }
        }
    }

    int simulate_operation() {
        auto_set_mode();
        int use_time = 0;

        if (mode == "heat") {
            while (current_temperature < target_temperature) {
                current_temperature += 1.0;
                use_time += 1;
            }
        } else if (mode == "cool") {
            while (current_temperature > target_temperature) {
                current_temperature -= 1.0;
                use_time += 1;
            }
        }

        return use_time;
    }
};