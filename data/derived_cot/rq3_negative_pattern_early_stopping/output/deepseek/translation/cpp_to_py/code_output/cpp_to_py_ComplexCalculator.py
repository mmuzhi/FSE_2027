class ComplexCalculator:
    @staticmethod
    def add(c1, c2):
        return c1 + c2

    @staticmethod
    def subtract(c1, c2):
        return c1 - c2

    @staticmethod
    def multiply(c1, c2):
        return c1 * c2

    @staticmethod
    def divide(c1, c2):
        den = c2.real ** 2 + c2.imag ** 2
        real = (c1.real * c2.real + c1.imag * c2.imag) / den
        imag = (c1.imag * c2.real - c1.real * c2.imag) / den
        return complex(real, imag)