class FitnessTracker:
    BMI_std = {
        "male": [20.0, 25.0],
        "female": [19.0, 24.0]
    }

    def __init__(self, height, weight, age, sex):
        self.height = height
        self.weight = weight
        self.age = age
        self.sex = sex

    @property
    def get_BMI(self):
        return self.weight / (self.height ** 2)

    def condition_judge(self):
        bmi = self.get_BMI
        bmi_range = self.BMI_std[self.sex]
        if bmi > bmi_range[1]:
            return 1
        elif bmi < bmi_range[0]:
            return -1
        else:
            return 0

    def calculate_calorie_intake(self):
        # Calculate Basal Metabolic Rate (BMR)
        if self.sex == "male":
            bmr = 10 * self.weight + 6.25 * self.height - 5 * self.age + 5
        else:
            bmr = 10 * self.weight + 6.25 * self.height - 5 * self.age - 161
        
        condition = self.condition_judge()
        if condition == 1:
            return bmr * 1.2
        elif condition == -1:
            return bmr * 1.6
        else:
            return bmr * 1.4