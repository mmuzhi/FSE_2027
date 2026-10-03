class BigNumCalculator:
    @staticmethod
    def add(num1, num2):
        max_length = max(len(num1), len(num2))
        num1_padded = '0' * (max_length - len(num1)) + num1
        num2_padded = '0' * (max_length - len(num2)) + num2

        carry = 0
        result = []
        for i in range(max_length - 1, -1, -1):
            digit_sum = (ord(num1_padded[i]) - ord('0')) + (ord(num2_padded[i]) - ord('0')) + carry
            carry = digit_sum // 10
            digit = digit_sum % 10
            result.insert(0, chr(digit + ord('0')))

        if carry > 0:
            result.insert(0, chr(carry + ord('0')))

        return ''.join(result)

    @staticmethod
    def subtract(num1, num2):
        num1_local = num1
        num2_local = num2
        negative = False

        if len(num1_local) < len(num2_local) or (len(num1_local) == len(num2_local) and num1_local < num2_local):
            num1_local, num2_local = num2_local, num1_local
            negative = True

        max_length = max(len(num1_local), len(num2_local))
        num1_local = '0' * (max_length - len(num1_local)) + num1_local
        num2_local = '0' * (max_length - len(num2_local)) + num2_local

        borrow = 0
        result = []
        for i in range(max_length - 1, -1, -1):
            digit_diff = (ord(num1_local[i]) - ord('0')) - (ord(num2_local[i]) - ord('0')) - borrow

            if digit_diff < 0:
                digit_diff += 10
                borrow = 1
            else:
                borrow = 0

            result.insert(0, chr(digit_diff + ord('0')))

        while len(result) > 1 and result[0] == '0':
            result.pop(0)

        if negative:
            result.insert(0, '-')

        return ''.join(result)

    @staticmethod
    def multiply(num1, num2):
        len1 = len(num1)
        len2 = len(num2)
        result = [0] * (len1 + len2)

        for i in range(len1 - 1, -1, -1):
            for j in range(len2 - 1, -1, -1):
                mul = (ord(num1[i]) - ord('0')) * (ord(num2[j]) - ord('0'))
                p1 = i + j
                p2 = i + j + 1
                total = mul + result[p2]

                result[p1] += total // 10
                result[p2] = total % 10

        result_str = ''
        leading_zero = True
        for num in result:
            if num == 0 and leading_zero:
                continue
            leading_zero = False
            result_str += str(num)

        return '0' if not result_str else result_str