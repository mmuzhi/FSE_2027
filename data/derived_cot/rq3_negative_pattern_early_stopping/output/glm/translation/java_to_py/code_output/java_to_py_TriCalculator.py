import math
from decimal import Decimal, localcontext, ROUND_HALF_UP

class TriCalculator:

    def cos(self, x: float) -> float:
        return self.round(self.taylor(x, 50), 10)

    def factorial(self, a: int) -> Decimal:
        result = Decimal(1)
        while a > 1:
            result *= Decimal(a)
            a -= 1
        return result

    def taylor(self, x: float, n: int) -> float:
        a = Decimal(1)
        x = x / 180 * math.pi
        count = 1
        for k in range(1, n):
            power = x ** (2 * k)
            if math.isinf(power) or math.isnan(power):
                raise ValueError("NaN or Infinity")
            with localcontext() as ctx:
                ctx.prec = 34
                term = Decimal(str(power)) / self.factorial(2 * k)
            if count % 2 != 0:
                a -= term
            else:
                a += term
            count += 1
        return float(a)

    def sin(self, x: float) -> float:
        x = x / 180 * math.pi
        g = 0.0
        t = x
        n = 1
        while abs(t) >= 1e-15:
            g += t
            n += 1
            t = -t * x * x / (2 * n - 1) / (2 * n - 2)
        return self.round(g, 10)

    def tan(self, x: float) -> float:
        cos_value = self.cos(x)
        if cos_value != 0:
            return self.round(self.sin(x) / cos_value, 10)
        else:
            return float('nan')

    def round(self, value: float, places: int) -> float:
        if math.isnan(value) or math.isinf(value):
            raise ValueError("NaN or Infinity")
        bd = Decimal(str(value))
        bd = bd.quantize(Decimal(10) ** -places, rounding=ROUND_HALF_UP)
        return float(bd)