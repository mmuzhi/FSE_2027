#include <string>
#include <vector>

class FitnessTracker {
private:
    double height;
    double weight;
    int age;
    std::string sex;
    static const std::vector<std::vector<double>> BMI_std;

public:
    explicit FitnessTracker(double height, double weight, int age, const std::string& sex)
        : height(height), weight(weight), age(age), sex(sex) {}

    double getBMI() const {
        return weight / (height * height);
    }

    int conditionJudge() const {
        const int index = (sex == "male") ? 0 : 1;
        const double BMI = getBMI();
        if (BMI > BMI_std[index][1]) {
            return 1;
        }
        else if (BMI < BMI_std[index][0]) {
            return -1;
        }
        return 0;
    }

    double calculateCalorieIntake() const {
        double BMR;
        if (sex == "male") {
            BMR = 10 * weight + 6.25 * height - 5 * age + 5;
        }
        else {
            BMR = 10 * weight + 6.25 * height - 5 * age - 161;
        }

        const int condition = conditionJudge();
        if (condition == 1) {
            return BMR * 1.2;
        }
        else if (condition == -1) {
            return BMR * 1.6;
        }
        return BMR * 1.4;
    }
};

// Static member initialization
const std::vector<std::vector<double>> FitnessTracker::BMI_std = {
    {20, 25},  // Male BMI standards
    {19, 24}   // Female BMI standards
};