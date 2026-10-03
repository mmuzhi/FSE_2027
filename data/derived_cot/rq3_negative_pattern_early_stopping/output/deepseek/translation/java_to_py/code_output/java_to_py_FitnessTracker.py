class FitnessTracker:
    def __init__(self, height: float, weight: float, age: int, sex: str):
        self.height = height
        self.weight = weight
        self.age = age
        self.sex = sex
        self.BMI_std = [[20, 25], [19, 24]]

    def getBMI(self) -> float:
        return self.weight / (self.height * self.height)

    def conditionJudge(self) -> int:
        BMI = self.getBMI()
        index = 0 if self.sex == "male" else 1
        if BMI > self.BMI_std[index][1]:
            return 1
        elif BMI < self.BMI_std[index][0]:
            return -1
        else:
            return 0

    def calculateCalorieIntake(self) -> float:
        if self.sex == "male":
            BMR = 10 * self.weight + 6.25 * self.height - 5 * self.age + 5
        else:
            BMR = 10 * self.weight + 6.25 * self.height - 5 * self.age - 161

        condition = self.conditionJudge()
        if condition == 1:
            return BMR * 1.2
        elif condition == -1:
            return BMR * 1.6
        else:
            return BMR * 1.4