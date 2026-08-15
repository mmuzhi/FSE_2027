import math
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN, localcontext, getcontext
from fractions import Fraction

getcontext().prec = 1000


class TriCalculator:
    def __init__(self):
        pass

    def cos(self, x):
        return self._round(self.taylor(x, 50), 10)

    def factorial(self, a):
        result = Decimal(1)
        while a > 1:
            result *= a
            a -= 1
        return result

    def taylor(self, x, n):
        a = Fraction(1, 1)
        x = x / 180 * math.pi
        count = 1
        with localcontext() as ctx:
            ctx.prec = 34
            ctx.rounding = ROUND_HALF_EVEN
            for k in range(1, n):
                term = Decimal(str(math.pow(x, 2 * k))) / self.factorial(2 * k)
                term_frac = Fraction(term)
                if count % 2 != 0:
                    a -= term_frac
                else:
                    a += term_frac
                count += 1
        return float(a)

    def sin(self, x):
        x = x / 180 * math.pi
        g = 0.0
        t = x
        n = 1
        while abs(t) >= 1e-15:
            g += t
            n += 1
            t = -t * x * x / (2 * n - 1) / (2 * n - 2)
        return self._round(g, 10)

    def tan(self, x):
        cos_value = self.cos(x)
        if cos_value != 0:
            return self._round(self.sin(x) / cos_value, 10)
        else:
            return float('nan')

    def _round(self, value, places):
        d = Decimal(str(value))
        exp = Decimal(1).scaleb(-places)
        d = d.quantize(exp, rounding=ROUND_HALF_UP)
        result = float(d)
        if result == 0.0:
            return 0.0
        return result