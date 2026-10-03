class Thermostat:
    def __init__(self, current_temperature: float, target_temperature: float, mode: str):
        self.current_temperature = current_temperature
        self.target_temperature = target_temperature
        self.mode = mode

    def get_target_temperature(self) -> float:
        return self.target_temperature

    def set_target_temperature(self, temperature: float) -> None:
        self.target_temperature = temperature

    def get_mode(self) -> str:
        return self.mode

    def set_mode(self, new_mode: str) -> bool:
        if new_mode == "heat" or new_mode == "cool":
            self.mode = new_mode
            return True
        return False

    def auto_set_mode(self) -> None:
        if self.current_temperature < self.target_temperature:
            self.mode = "heat"
        else:
            self.mode = "cool"

    def auto_check_conflict(self) -> bool:
        if self.current_temperature > self.target_temperature:
            if self.mode == "cool":
                return True
            else:
                self.auto_set_mode()
                return False
        else:
            if self.mode == "heat":
                return True
            else:
                self.auto_set_mode()
                return False

    def simulate_operation(self) -> int:
        self.auto_set_mode()
        use_time = 0
        if self.mode == "heat":
            while self.current_temperature < self.target_temperature:
                self.current_temperature += 1.0
                use_time += 1
        else:
            while self.current_temperature > self.target_temperature:
                self.current_temperature -= 1.0
                use_time += 1
        return use_time