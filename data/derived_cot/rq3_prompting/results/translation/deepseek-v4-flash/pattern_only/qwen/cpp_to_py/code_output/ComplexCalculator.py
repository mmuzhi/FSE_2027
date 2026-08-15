class ComplexCalculator:
    @staticmethod
    def add(c1, c2):
        return complex(c1.real + c2.real, c1.imag + c2.imag)

    @staticmethod
    def subtract(c1, c2):
        return complex(c1.real - c2.real, c1.imag - c2.imag)

    @staticmethod
    def multiply(c1, c2):
        real = c1.real * c2.real - c1.imag * c2.imag
        imag = c1.real * c2.imag + c1.imag * c2.real
        return complex(real, imag)

    @staticmethod
    def divide(c1, c2):
        denominator = c2.real * c2.real + c2.imag * c2.imag
        real_num = c1.real * c2.real + c1.imag * c2.imag
        imag_num = c1.imag * c2.real - c1.real * c2.imag

        if denominator == 0.0:
            if real_num == 0.0 or real_num != real_num:
                real = float('nan')
            elif real_num > 0.0:
                real = float('inf')
            else:
                real = float('-inf')

            if imag_num == 0.0 or imag_num != imag_num:
                imag = float('nan')
            elif imag_num > 0.0:
                imag = float('inf')
            else:
                imag = float('-inf')
        else:
            real = real_num / denominator
            imag = imag_num / denominator

        return complex(real, imag)