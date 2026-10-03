import math
from decimal import Decimal, getcontext, localcontext, ROUND_HALF_EVEN, ROUND_HALF_UP

class TriCalculator:
    def __init__(self):
        pass

    def cos(self, x):
        return self.round(self.taylor(x, 50), 10)

    def factorial(self, a):
        result = Decimal(1)
        while a > 1:
            result *= Decimal(a)
            a -= 1
        return result

    def taylor(self, x, n):
        a = Decimal(1)
        x_rad = x / 180.0 * math.pi
        count = 1
        for k in range(1, n):
            with localcontext() as ctx:
                ctx.prec = 34
                ctx.rounding = ROUND_HALF_EVEN
                term = Decimal(str(math.pow(x_rad, 2 * k))) / self.factorial(2 * k)
            if count % 2 != 0:
                a -= term
            else:
                a += term
            count += 1
        return float(a)

    def sin(self, x):
        x_rad = x / 180.0 * math.pi
        g = 0.0
        t = x_rad
        n = 1
        while abs(t) >= 1e-15:
            g += t
            n += 1
            t = -t * x_rad * x_rad / (2 * n - 1) / (2 * n - 2)
        return self.round(g, 10)

    def tan(self, x):
        cos_val = self.cos(x)
        if cos_val != 0:
            return self.round(self.sin(x) / cos_val, 10)
        else:
            return float('nan')

    def round(self, value, places):
        bd = Decimal(str(value))
        quantize_str = '0.' + '0' * places
        bd = bd.quantize(Decimal(quantize_str), rounding=ROUND_HALF_UP)
        return float(bd)