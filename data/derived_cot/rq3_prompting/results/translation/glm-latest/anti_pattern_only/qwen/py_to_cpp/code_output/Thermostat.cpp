#include <string>
#include <utility>

class Thermostat {
public:
    // Public data members mirror Python's freely accessible attributes.
    double current_temperature;
    double target_temperature;
    std::string mode;

    // Initialize a Thermostat with the current temperature, target temperature,
    // and operating mode.
    Thermostat(double current_temperature, double target_temperature, std::string mode)
        : current_temperature(current_temperature),
          target_temperature(target_temperature),
          mode(std::move(mode)) {}

    // Get the target temperature.
    double get_target_temperature() const {
        return target_temperature;
    }

    // Set the target temperature.
    void set_target_temperature(double temperature) {
        target_temperature = temperature;
    }

    // Get the current work mode.
    const std::string& get_mode() const {
        return mode;
    }

    // Set the current work mode; only 'heat' and 'cool' are accepted.
    // Returns false when the mode is invalid (mirroring the Python behavior).
    bool set_mode(const std::string& mode) {
        if (mode == "heat" || mode == "cool") {
            this->mode = mode;
            return true;
        }
        return false;
    }

    // Automatically set the operating mode: 'heat' if the current temperature
    // is lower than the target temperature, 'cool' otherwise.
    void auto_set_mode() {
        if (current_temperature < target_temperature) {
            mode = "heat";
        } else {
            mode = "cool";
        }
    }

    // Check for a conflict between the operating mode and the relationship
    // between the current and target temperatures. If there is a conflict,
    // the mode is adjusted automatically. Returns true when there is no
    // conflict, false otherwise.
    bool auto_check_conflict() {
        if (current_temperature > target_temperature) {
            if (mode == "cool") {
                return true;
            } else {
                auto_set_mode();
                return false;
            }
        } else {
            if (mode == "heat") {
                return true;
            } else {
                auto_set_mode();
                return false;
            }
        }
    }

    // Simulate the operation of the Thermostat: auto-set the mode, then adjust
    // the current temperature toward the target temperature. Returns the time
    // (number of steps) it took to complete the simulation.
    int simulate_operation() {
        auto_set_mode();
        int use_time = 0;
        if (mode == "heat") {
            while (current_temperature < target_temperature) {
                current_temperature += 1;
                use_time += 1;
            }
        } else {
            while (current_temperature > target_temperature) {
                current_temperature -= 1;
                use_time += 1;
            }
        }
        return use_time;
    }
};