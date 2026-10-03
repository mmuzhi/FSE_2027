class Thermostat:
    def __init__(self, currentTemperature, targetTemperature, mode):
        self.currentTemperature = currentTemperature
        self._targetTemperature = targetTemperature
        self._mode = mode

    def getTargetTemperature(self):
        return self._targetTemperature

    def setTargetTemperature(self, temperature):
        self._targetTemperature = temperature

    def getMode(self):
        return self._mode

    def setMode(self, mode):
        if mode == "heat" or mode == "cool":
            self._mode = mode
            return True
        else:
            return False

    def autoSetMode(self):
        if self.currentTemperature < self._targetTemperature:
            self._mode = "heat"
        else:
            self._mode = "cool"

    def autoCheckConflict(self):
        if self.currentTemperature > self._targetTemperature:
            if self._mode == "cool":
                return True
            else:
                self.autoSetMode()
                return False
        else:
            if self._mode == "heat":
                return True
            else:
                self.autoSetMode()
                return False

    def simulateOperation(self):
        self.autoSetMode()
        useTime = 0
        if self._mode == "heat":
            while self.currentTemperature < self._targetTemperature:
                self.currentTemperature += 1.0
                useTime += 1
        else:
            while self.currentTemperature > self._targetTemperature:
                self.currentTemperature -= 1.0
                useTime += 1
        return useTime