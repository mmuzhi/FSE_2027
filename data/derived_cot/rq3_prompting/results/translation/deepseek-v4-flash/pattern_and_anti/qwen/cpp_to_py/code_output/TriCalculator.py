import math

class TriCalculator:
    PI = 3.14159265358979323846

    def __init__(self):
        pass

    def round(self, value, precision):
        if math.isnan(value) or math.isinf(value):
            return value
        factor = 10.0 ** precision
        product = value * factor
        if math.isnan(product) or math.isinf(product):
            return product
        if value >= 0:
            result = math.floor(product + 0.5) / factor
        else:
            result = math.ceil(product - 0.5) / factor
        if result == 0.0 and math.copysign(1.0, value) < 0:
            return -0.0
        return result

    def factorial(self, a):
        if a < 0:
            return 0
        if a == 0:
            return 1
        b = 1
        for i in range(1, a + 1):
            b *= i
            b &= 0xFFFFFFFF
            if b >= 0x80000000:
                b -= 0x100000000
        return b

    def taylor(self, x, n):
        a = 0.0
        x = x / 180.0 * self.PI
        for k in range(n):
            term = (x ** (2 * k)) / self.factorial(2 * k)
            if k % 2 == 0:
                a += term
            else:
                a -= term
        return a

    def cos(self, x):
        result = self.taylor(x, 17)
        print(f"Taylor result for cos: {result:.6g}", flush=True)
        return self.round(result, 10)

    def sin(self, x):
        x = x / 180.0 * self.PI
        g = 0.0
        t = x
        n = 1
        while abs(t) >= 1e-15:
            g += t
            n += 1
            t = -t * x * x / ((2 * n - 1) * (2 * n - 2))
        return self.round(g, 10)

    def tan(self, x):
        cosine = self.cos(x)
        if abs(cosine) > 0.01:
            result = self.sin(x) / cosine
            return self.round(result, 10)
        else:
            return float('nan')