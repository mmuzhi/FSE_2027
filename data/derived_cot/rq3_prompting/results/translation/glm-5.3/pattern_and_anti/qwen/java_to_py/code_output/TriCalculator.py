import math
from decimal import Decimal, Context, localcontext, ROUND_HALF_EVEN, ROUND_HALF_UP, MAX_PREC

# Mirrors java.math.MathContext.DECIMAL128 (34 digits, HALF_EVEN)
DECIMAL128 = Context(prec=34, rounding=ROUND_HALF_EVEN)


class TriCalculator:

    def __init__(self):
        pass

    def cos(self, x):
        return self._round(self.taylor(x, 50), 10)

    def factorial(self, a):
        # BigDecimal arithmetic is exact (unlimited precision)
        with localcontext() as ctx:
            ctx.prec = MAX_PREC
            result = Decimal(1)
            while a > 1:
                result = result * Decimal(a)
                a -= 1
            return result

    def taylor(self, x, n):
        with localcontext() as ctx:
            ctx.prec = MAX_PREC
            a = Decimal(1)
            x = x / 180 * math.pi
            count = 1
            for k in range(1, n):
                term = DECIMAL128.divide(self._bd_value_of(math.pow(x, 2 * k)),
                                         self.factorial(2 * k))
                if count % 2 != 0:
                    a = a - term
                else:
                    a = a + term
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

    @staticmethod
    def _bd_value_of(x):
        # Mirrors java.math.BigDecimal.valueOf(double):
        # uses the shortest round-trip decimal string; rejects NaN/Infinity.
        if math.isnan(x) or math.isinf(x):
            raise ValueError("Infinite or NaN")
        return Decimal(str(x))

    def _round(self, value, places):
        # Mirrors BigDecimal.valueOf(value).setScale(places, HALF_UP).doubleValue()
        with localcontext() as ctx:
            ctx.prec = MAX_PREC
            bd = self._bd_value_of(value)
            bd = bd.quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP)
            return float(bd)