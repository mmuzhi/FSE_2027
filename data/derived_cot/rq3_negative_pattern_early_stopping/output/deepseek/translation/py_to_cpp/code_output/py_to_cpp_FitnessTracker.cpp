#include <string>
#include <cmath>

class FitnessTracker {
private:
    double height;
    double weight;
    double age;
    std::string sex;
    int male_bmi_low = 20;
    int male_bmi_high = 25;
    int female_bmi_low = 19;
    int female_bmi_high = 24;

public:
    FitnessTracker(double height, double weight, double age, const std::string& sex)
        : height(height), weight(weight), age(age), sex(sex) {}

    double get_BMI() {
        return weight / (height * height);
    }

    int condition_judge() {
        double bmi = get_BMI();
        int low, high;
        if (sex == "male") {
            low = male_bmi_low;
            high = male_bmi_high;
        } else {
            low = female_bmi_low;
            high = female_bmi_high;
        }
        if (bmi > high)
            return 1;           // too fat
        else if (bmi < low)
            return -1;          // too thin
        else
            return 0;           // normal
    }

    double calculate_calorie_intake() {
        double BMR;
        if (sex == "male")
            BMR = 10 * weight + 6.25 * height - 5 * age + 5;
        else
            BMR = 10 * weight + 6.25 * height - 5 * age - 161;

        int cond = condition_judge();
        double calorie_intake;
        if (cond == 1)
            calorie_intake = BMR * 1.2;
        else if (cond == -1)
            calorie_intake = BMR * 1.6;
        else
            calorie_intake = BMR * 1.4;
        return calorie_intake;
    }
};