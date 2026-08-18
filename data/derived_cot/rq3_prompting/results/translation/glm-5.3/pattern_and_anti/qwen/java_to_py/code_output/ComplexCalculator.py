import struct


def _double_compare_zero(a: float, b: float) -> bool:
    """True iff Double.compare(a, b) == 0 (bit-identical doubles: NaN==NaN, -0.0 != 0.0)."""
    return struct.pack('>d', a) == struct.pack('>d', b)


class ComplexCalculator:

    def add(self, c1, c2):
        real = c1.getReal() + c2.getReal()
        imaginary = c1.getImaginary() + c2.getImaginary()
        return ComplexCalculator.ComplexNumber(real, imaginary)

    def subtract(self, c1, c2):
        real = c1.getReal() - c2.getReal()
        imaginary = c1.getImaginary() - c2.getImaginary()
        return ComplexCalculator.ComplexNumber(real, imaginary)

    def multiply(self, c1, c2):
        real = c1.getReal() * c2.getReal() - c1.getImaginary() * c2.getImaginary()
        imaginary = c1.getReal() * c2.getImaginary() + c1.getImaginary() * c2.getReal()
        return ComplexCalculator.ComplexNumber(real, imaginary)

    def divide(self, c1, c2):
        denominator = c2.getReal() * c2.getReal() + c2.getImaginary() * c2.getImaginary()
        real = (c1.getReal() * c2.getReal() + c1.getImaginary() * c2.getImaginary()) / denominator
        imaginary = (c1.getImaginary() * c2.getReal() - c1.getReal() * c2.getImaginary()) / denominator
        return ComplexCalculator.ComplexNumber(real, imaginary)

    class ComplexNumber:
        __slots__ = ("real", "imaginary")

        def __init__(self, real, imaginary):
            self.real = real
            self.imaginary = imaginary

        def getReal(self):
            return self.real

        def getImaginary(self):
            return self.imaginary

        def __eq__(self, obj):
            if self is obj:
                return True
            if obj is None or type(self) is not type(obj):
                return False
            return (_double_compare_zero(obj.real, self.real)
                    and _double_compare_zero(obj.imaginary, self.imaginary))

        def __ne__(self, obj):
            result = self.__eq__(obj)
            if result is NotImplemented:
                return result
            return not result

        def __hash__(self):
            # Java objects remain hashable; hash on bit patterns keeps NaN consistent with __eq__.
            return hash((struct.pack('>d', self.real), struct.pack('>d', self.imaginary)))

        def __repr__(self):
            return (str(self.real) + ("+" if self.imaginary >= 0 else "")
                    + str(self.imaginary) + "j")

        def toString(self):
            return self.__repr__()