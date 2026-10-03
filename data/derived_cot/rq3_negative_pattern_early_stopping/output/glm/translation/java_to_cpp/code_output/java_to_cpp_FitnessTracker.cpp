#include <string>
#include <utility>

class FitnessTracker {
private:
    double height;
    double weight;
    int age;
    std::string sex;
    double BMI_std[2][2] = { {20, 25}, {19, 24} };

public:
    FitnessTracker(double height, double weight, int age, std::string sex)
        : height(height), weight(weight), age(age), sex(std::move(sex)) {}

    double getBMI() const {
        return weight / (height * height);
    }

    int conditionJudge() const {
        double BMI = getBMI();
        int index = (sex == "male") ? 0 : 1;
        if (BMI > BMI_std[index][1]) {
            return 1;
        } else if (BMI < BMI_std[index][0]) {
            return -1;
        } else {
            return 0;
        }
    }

    double calculateCalorieIntake() const {
        double BMR;
        if (sex == "male") {
            BMR = 10 * weight + 6.25 * height - 5 * age + 5;
        } else {
            BMR = 10 * weight + 6.25 * height - 5 * age - 161;
        }

        int condition = conditionJudge();
        if (condition == 1) {
            return BMR * 1.2;
        } else if (condition == -1) {
            return BMR * 1.6;
        } else {
            return BMR * 1.4;
        }
    }
};