class FitnessTracker:
    def __init__(self, height, weight, age, sex):
        self.height = height
        self.weight = weight
        self.age = age
        self.sex = sex
        self.BMI_std = [[20, 25], [19, 24]]  # BMI standards for male and female

    def get_bmi(self):
        return self.weight / (self.height ** 2)

    def condition_judge(self):
        bmi = self.get_bmi()
        index = 0 if self.sex == "male" else 1
        if bmi > self.BMI_std[index][1]:
            return 1
        elif bmi < self.BMI_std[index][0]:
            return -1
        else:
            return 0

    def calculate_calorie_intake(self):
        bmr = 10 * self.weight + 6.25 * self.height - 5 * self.age + (5 if self.sex == "male" else -161)
        condition = self.condition_judge()
        if condition == 1:
            return bmr * 1.2
        elif condition == -1:
            return bmr * 1.6
        else:
            return bmr * 1.4