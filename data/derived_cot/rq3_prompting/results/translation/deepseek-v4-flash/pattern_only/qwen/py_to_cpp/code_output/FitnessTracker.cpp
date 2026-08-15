#include <string>
#include <vector>
#include <map>
#include <stdexcept>

class FitnessTracker {
public:
    double height;
    double weight;
    int age;
    std::string sex;
    std::vector<std::map<std::string, std::vector<double>>> BMI_std;

    FitnessTracker(double height, double weight, int age, const std::string& sex)
        : height(height), weight(weight), age(age), sex(sex) {
        BMI_std = {
            {{"male", {20.0, 25.0}}},
            {{"female", {19.0, 24.0}}}
        };
    }

    double get_BMI() const {
        if (height == 0.0) {
            throw std::runtime_error("division by zero");
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
            return 1;
        } else if (BMI < BMI_range[0]) {
            return -1;
        } else {
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
        int condition = condition_judge();
        double calorie_intake;
        if (condition == 1) {
            calorie_intake = BMR * 1.2;
        } else if (condition == -1) {
            calorie_intake = BMR * 1.6;
        } else {
            calorie_intake = BMR * 1.4;
        }
        return calorie_intake;
    }
};