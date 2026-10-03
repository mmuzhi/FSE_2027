class FitnessTracker:
    BMI_std = {
        "male": [20.0, 25.0],
        "female": [19.0, 24.0]
    }

    def __init__(self, height: float, weight: float, age: int, sex: str) -> None:
        self.height = height
        self.weight = weight
        self.age = age
        self.sex = sex

    def get_BMI(self) -> float:
        """Return the BMI value: weight / height^2."""
        return self.weight / (self.height * self.height)

    def condition_judge(self) -> int:
        """
        Return:
         1 if BMI > upper threshold,
        -1 if BMI < lower threshold,
         0 otherwise.
        """
        bmi = self.get_BMI()
        lower, upper = self.BMI_std[self.sex]
        if bmi > upper:
            return 1
        elif bmi < lower:
            return -1
        else:
            return 0

    def calculate_calorie_intake(self) -> float:
        """
        Calculate recommended daily calorie intake based on BMR and body condition.
        BMR formula differs for male / female.
        Condition adjusts multiplier:
          overweight -> *1.2
          underweight -> *1.6
          normal      -> *1.4
        """
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