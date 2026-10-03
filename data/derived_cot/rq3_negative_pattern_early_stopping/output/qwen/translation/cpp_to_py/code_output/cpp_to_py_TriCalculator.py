import math
import sys

class TriCalculator:
    PI = 3.14159265358979323846

    @staticmethod
    def round(value, precision):
        factor = 10.0 ** precision
        return round(value * factor) / factor

    def __init__(self):
        pass

    def cos(self, x):
        result = self.taylor(x, 17)
        print(f"Taylor result for cos: {result}", file=sys.stdout)
        return self.round(result, 10)

    @staticmethod
    def factorial(a):
        if a < 0:
            return 0
        if a == 0:
            return 1
        b = 1
        for i in range(1, a + 1):
            b *= i
        return b

    @staticmethod
    def taylor(x, n):
        x_rad = x * math.pi / 180.0
        total = 0.0
        sign = 1
        for k in range(n):
            term = (x_rad ** (2 * k)) / TriCalculator.factorial(2 * k)
            if k % 2 == 0:
                total += term
            else:
                total -= term
        return total

    def sin(self, x):
        x_rad = x * math.pi / 180.0
        total = 0.0
        term = x_rad
        n = 1
        while abs(term) >= 1e-15:
            total += term
            n += 1
            term = -term * x_rad * x_rad / ((2 * n - 1) * (2 * n - 2))
        return self.round(total, 10)

    def tan(self, x):
        cosine = self.cos(x)
        if abs(cosine) > 0.01:
            return self.round(sin(x) / cosine, 10)
        else:
            return float('nan')