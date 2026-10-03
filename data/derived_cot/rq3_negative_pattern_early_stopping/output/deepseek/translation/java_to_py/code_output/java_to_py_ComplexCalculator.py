class ComplexCalculator:
    class ComplexNumber:
        def __init__(self, real: float, imaginary: float):
            self._real = real
            self._imaginary = imaginary

        def get_real(self) -> float:
            return self._real

        def get_imaginary(self) -> float:
            return self._imaginary

        def __eq__(self, other: object) -> bool:
            if self is other:
                return True
            if other is None or type(self) != type(other):
                return False
            that = other
            return (ComplexCalculator._double_compare(self._real, that._real) == 0 and
                    ComplexCalculator._double_compare(self._imaginary, that._imaginary) == 0)

        def __repr__(self) -> str:
            return f"{self._real}{'+' if self._imaginary >= 0 else ''}{self._imaginary}j"

        def __str__(self) -> str:
            return self.__repr__()

    @staticmethod
    def _double_compare(d1: float, d2: float) -> int:
        if d1 < d2:
            return -1
        if d1 > d2:
            return 1
        import math
        if d1 == d2:
            if d1 == 0.0:
                if math.copysign(1.0, d1) != math.copysign(1.0, d2):
                    return 1  # 0.0 > -0.0 according to Java
            return 0
        if math.isnan(d1) and math.isnan(d2):
            return 0
        return -1

    def add(self, c1: ComplexNumber, c2: ComplexNumber) -> ComplexNumber:
        real = c1.get_real() + c2.get_real()
        imaginary = c1.get_imaginary() + c2.get_imaginary()
        return self.ComplexNumber(real, imaginary)

    def subtract(self, c1: ComplexNumber, c2: ComplexNumber) -> ComplexNumber:
        real = c1.get_real() - c2.get_real()
        imaginary = c1.get_imaginary() - c2.get_imaginary()
        return self.ComplexNumber(real, imaginary)

    def multiply(self, c1: ComplexNumber, c2: ComplexNumber) -> ComplexNumber:
        real = c1.get_real() * c2.get_real() - c1.get_imaginary() * c2.get_imaginary()
        imaginary = c1.get_real() * c2.get_imaginary() + c1.get_imaginary() * c2.get_real()
        return self.ComplexNumber(real, imaginary)

    def divide(self, c1: ComplexNumber, c2: ComplexNumber) -> ComplexNumber:
        denominator = c2.get_real() * c2.get_real() + c2.get_imaginary() * c2.get_imaginary()
        real = (c1.get_real() * c2.get_real() + c1.get_imaginary() * c2.get_imaginary()) / denominator
        imaginary = (c1.get_imaginary() * c2.get_real() - c1.get_real() * c2.get_imaginary()) / denominator
        return self.ComplexNumber(real, imaginary)