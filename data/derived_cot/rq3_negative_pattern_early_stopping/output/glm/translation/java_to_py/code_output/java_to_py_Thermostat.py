class Thermostat:
    def __init__(self, current_temperature: float, target_temperature: float, mode: str):
        self.current_temperature = current_temperature
        self._target_temperature = target_temperature
        self._mode = mode

    def get_target_temperature(self) -> float:
        return self._target_temperature

    def set_target_temperature(self, temperature: float) -> None:
        self._target_temperature = temperature

    def get_mode(self) -> str:
        return self._mode

    def set_mode(self, mode: str) -> bool:
        if mode == "heat" or mode == "cool":
            self._mode = mode
            return True
        else:
            return False

    def auto_set_mode(self) -> None:
        if self.current_temperature < self._target_temperature:
            self._mode = "heat"
        else:
            self._mode = "cool"

    def auto_check_conflict(self) -> bool:
        if self.current_temperature > self._target_temperature:
            if self._mode == "cool":
                return True
            else:
                self.auto_set_mode()
                return False
        else:
            if self._mode == "heat":
                return True
            else:
                self.auto_set_mode()
                return False

    def simulate_operation(self) -> int:
        self.auto_set_mode()
        use_time = 0
        if self._mode == "heat":
            while self.current_temperature < self._target_temperature:
                self.current_temperature += 1
                use_time += 1
        else:
            while self.current_temperature > self._target_temperature:
                self.current_temperature -= 1
                use_time += 1
        return use_time