class ComplexCalculator:

    @staticmethod
    def add(c1, c2):
        real = c1.real + c2.real
        imaginary = c1.imaginary + c2.imaginary
        return ComplexNumber(real, imaginary)

    @staticmethod
    def subtract(c1, c2):
        real = c1.real - c2.real
        imaginary = c1.imaginary - c2.imaginary
        return ComplexNumber(real, imaginary)

    @staticmethod
    def multiply(c1, c2):
        real = c1.real * c2.real - c1.imaginary * c2.imaginary
        imaginary = c1.real * c2.imaginary + c1.imaginary * c2.real
        return ComplexNumber(real, imaginary)

    @staticmethod
    def divide(c1, c2):
        denominator = c2.real * c2.real + c2.imaginary * c2.imaginary
        real = (c1.real * c2.real + c1.imaginary * c2.imaginary) / denominator
        imaginary = (c1.imaginary * c2.real - c1.real * c2.imaginary) / denominator
        return ComplexNumber(real, imaginary)

    class ComplexNumber:
        def __init__(self, real, imaginary):
            self.real = real
            self.imaginary = imaginary

        @property
        def real(self):
            return self._real

        @real.setter
        def real(self, value):
            self._real = value

        @property
        def imaginary(self):
            return self._imaginary

        @imaginary.setter
        def imaginary(self, value):
            self._imaginary = value

        def __eq__(self, other):
            if not isinstance(other, ComplexCalculator.ComplexNumber):
                return NotImplemented
            return (self.real == other.real) and (self.imaginary == other.imaginary)

        def __repr__(self):
            if self.imaginary == 0:
                return f"{self.real}"
            elif self.real == 0:
                if self.imaginary < 0:
                    return f"-{abs(self.imaginary)}j"
                else:
                    return f"{self.imaginary}j"
            else:
                if self.imaginary < 0:
                    return f"{self.real} - {abs(self.imaginary)}j"
                else:
                    return f"{self.real} + {self.imaginary}j"

        @staticmethod
        def parse_complex_number(s):
            # This is not used in the provided operations but kept for completeness if needed.
            pass