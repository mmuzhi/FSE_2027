#include <string>
#include <utility>
#include <vector>

class FitnessTracker {
public:
    FitnessTracker(double height, double weight, int age, const std::string& sex)
        : height(height), weight(weight), age(age), sex(sex),
          BMI_std{{"male", {20, 25}}, {"female", {19, 24}}} {}

    double get_BMI() const {
        return weight / (height * height);
    }

    int condition_judge() const {
        double BMI = get_BMI();
        std::pair<double, double> BMI_range;
        if (sex == "male") {
            BMI_range = BMI_std[0].second;
        } else {
            BMI_range = BMI_std[1].second;
        }
        if (BMI > BMI_range.second) {
            // too fat
            return 1;
        } else if (BMI < BMI_range.first) {
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
    int age;
    std::string sex;
    std::vector<std::pair<std::string, std::pair<double, double>>> BMI_std;
};