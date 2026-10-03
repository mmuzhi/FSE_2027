class BigNumCalculator:
    @staticmethod
    def add(num1: str, num2: str) -> str:
        max_length = max(len(num1), len(num2))
        num1_padded = '0' * (max_length - len(num1)) + num1
        num2_padded = '0' * (max_length - len(num2)) + num2

        carry = 0
        result = []
        for i in range(max_length - 1, -1, -1):
            digit_sum = (ord(num1_padded[i]) - ord('0')) + (ord(num2_padded[i]) - ord('0')) + carry
            carry = digit_sum // 10
            digit = digit_sum % 10
            result.append(chr(digit + ord('0')))
        if carry:
            result.append(chr(carry + ord('0')))
        return ''.join(reversed(result))

    @staticmethod
    def subtract(num1: str, num2: str) -> str:
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
            result.append(chr(digit_diff + ord('0')))
        result_str = ''.join(reversed(result))
        while len(result_str) > 1 and result_str[0] == '0':
            result_str = result_str[1:]
        if negative:
            result_str = '-' + result_str
        return result_str

    @staticmethod
    def multiply(num1: str, num2: str) -> str:
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

        parts = []
        leading_zero = True
        for num in result:
            if num == 0 and leading_zero:
                continue
            leading_zero = False
            parts.append(str(num))
        return '0' if not parts else ''.join(parts)