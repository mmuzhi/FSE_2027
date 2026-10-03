class FitnessTracker:
    _BMI_std = {
        "male": [20.0, 25.0],
        "female": [19.0, 24.0]
    }

    def __init__(self, height: float, weight: float, age: int, sex: str):
        self.height = height
        self.weight = weight
        self.age = age
        self.sex = sex

    def get_BMI(self) -> float:
        return self.weight / (self.height * self.height)

    def condition_judge(self) -> int:
        BMI = self.get_BMI()
        BMI_range = self._BMI_std[self.sex]  # KeyError if sex not found, same as C++ .at()
        if BMI > BMI_range[1]:
            return 1
        elif BMI < BMI_range[0]:
            return -1
        else:
            return 0

    def calculate_calorie_intake(self) -> float:
        if self.sex == "male":
            BMR = 10 * self.weight + 6.25 * self.height - 5 * self.age + 5
        else:
            BMR = 10 * self.weight + 6.25 * self.height - 5 * self.age - 161

        condition = self.condition_judge()
        if condition == 1:
            calorie_intake = BMR * 1.2
        elif condition == -1:
            calorie_intake = BMR * 1.6
        else:
            calorie_intake = BMR * 1.4
        return calorie_intake