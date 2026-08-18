#include <string>
#include <vector>
#include <map>
#include <stdexcept>

class FitnessTracker {
public:
    FitnessTracker(double height, double weight, double age, const std::string& sex)
        : height(height), weight(weight), age(age), sex(sex) {
        // BMI_std mirrors the Python list of dicts: male is 20-25, female is 19-24.
        BMI_std = {
            {{"male",   {20, 25}}},
            {{"female", {19, 24}}}
        };
    }

    double get_BMI() const {
        if (height == 0) {
            // Python raises ZeroDivisionError here; mirror it.
            throw std::runtime_error("ZeroDivisionError: float division by zero");
        }
        return weight / (height * height);
    }

    int condition_judge() const {
        double BMI = get_BMI();
        std::vector<double> BMI_range;
        if (sex == "male") {
            BMI_range = BMI_std[0].at("male");
        } else {
            BMI_range = BMI_std[1].at("female");
        }
        if (BMI > BMI_range[1]) {
            // too fat
            return 1;
        } else if (BMI < BMI_range[0]) {
            // too thin
            return -1;
        } else {
            // normal
            return 0;
        }
    }

    double calculate_calorie_intake() const {
        double BMR;
        if (sex == "male") {
            BMR = 10 * weight + 6.25 * height - 5 * age + 5;
        } else {
            BMR = 10 * weight + 6.25 * height - 5 * age - 161;
        }
        double calorie_intake;
        if (condition_judge() == 1) {
            calorie_intake = BMR * 1.2;  // Sedentary lifestyle
        } else if (condition_judge() == -1) {
            calorie_intake = BMR * 1.6;  // Active lifestyle
        } else {
            calorie_intake = BMR * 1.4;  // Moderate lifestyle
        }
        return calorie_intake;
    }

private:
    double height;
    double weight;
    double age;
    std::string sex;
    std::vector<std::map<std::string, std::vector<double>>> BMI_std;
};