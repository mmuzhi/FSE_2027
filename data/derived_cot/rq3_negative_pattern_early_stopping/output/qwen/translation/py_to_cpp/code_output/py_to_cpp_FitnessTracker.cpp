#include <iostream>
#include <map>
#include <string>

class FitnessTracker {
private:
    double height;
    double weight;
    int age;
    std::string sex;
    std::map<std::string, std::pair<double, double>> BMI_std;

public:
    FitnessTracker(double height, double weight, int age, std::string sex) {
        this->height = height;
        this->weight = weight;
        this->age = age;
        this->sex = sex;
        BMI_std["male"] = {20, 25};
        BMI_std["female"] = {19, 24};
    }

    double get_BMI() const {
        return weight / (height * height);
    }

    int condition_judge() const {
        double BMI = get_BMI();
        std::pair<double, double> BMI_range = BMI_std.at(sex);
        if (BMI > BMI_range.second) {
            return 1;
        } else if (BMI < BMI_range.first) {
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

int main() {
    // Example usage
    FitnessTracker tracker(1.8, 70, 20, "male");
    std::cout << "BMI: " << tracker.get_BMI() << std::endl;
    std::cout << "Condition: " << tracker.condition_judge() << std::endl;
    std::cout << "Calorie Intake: " << tracker.calculate_calorie_intake() << std::endl;
    return 0;
}