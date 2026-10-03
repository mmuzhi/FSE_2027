class Thermostat:
    def __init__(self, current_temperature, target_temperature, mode):
        self.current_temperature = current_temperature
        self.target_temperature = target_temperature
        self.mode = mode

    def get_target_temperature(self):
        return self.target_temperature

    def set_target_temperature(self, temperature):
        self.target_temperature = temperature

    def get_mode(self):
        return self.mode

    def set_mode(self, new_mode):
        if new_mode in ["heat", "cool"]:
            self.mode = new_mode
            return True
        return False

    def auto_set_mode(self):
        if self.current_temperature < self.target_temperature:
            self.mode = "heat"
        else:
            self.mode = "cool"

    def auto_check_conflict(self):
        if self.current_temperature > self.target_temperature:
            if self.mode == "cool":
                return True
            else:
                self.auto_set_mode()
                return False
        elif self.current_temperature < self.target_temperature:
            if self.mode == "heat":
                return True
            else:
                self.auto_set_mode()
                return False
        else:
            return False  # No conflict when temperatures are equal

    def simulate_operation(self):
        self.auto_set_mode()
        use_time = 0
        if self.mode == "heat":
            while self.current_temperature < self.target_temperature:
                self.current_temperature += 1
                use_time += 1
        elif self.mode == "cool":
            while self.current_temperature > self.target_temperature:
                self.current_temperature -= 1
                use_time += 1
        return use_time