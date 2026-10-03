class BigNumCalculator:

    @staticmethod
    def add(num1, num2):
        max_length = max(len(num1), len(num2))
        num1 = num1.zfill(max_length)
        num2 = num2.zfill(max_length)

        carry = 0
        result = []
        for i in range(max_length - 1, -1, -1):
            digit_sum = int(num1[i]) + int(num2[i]) + carry
            carry = digit_sum // 10
            digit = digit_sum % 10
            result.append(str(digit))

        if carry > 0:
            result.append(str(carry))

        return "".join(reversed(result))

    @staticmethod
    def subtract(num1, num2):
        negative = False
        if len(num1) < len(num2) or (len(num1) == len(num2) and num1 < num2):
            num1, num2 = num2, num1
            negative = True

        max_length = max(len(num1), len(num2))
        num1 = num1.zfill(max_length)
        num2 = num2.zfill(max_length)

        borrow = 0
        result = []
        for i in range(max_length - 1, -1, -1):
            digit_diff = int(num1[i]) - int(num2[i]) - borrow

            if digit_diff < 0:
                digit_diff += 10
                borrow = 1
            else:
                borrow = 0

            result.append(str(digit_diff))

        result_str = "".join(reversed(result)).lstrip('0')
        if not result_str:
            result_str = '0'

        if negative:
            result_str = '-' + result_str

        return result_str

    @staticmethod
    def multiply(num1, num2):
        len1 = len(num1)
        len2 = len(num2)
        result = [0] * (len1 + len2)

        for i in range(len1 - 1, -1, -1):
            for j in range(len2 - 1, -1, -1):
                mul = int(num1[i]) * int(num2[j])
                p1 = i + j
                p2 = i + j + 1
                total = mul + result[p2]

                result[p1] += total // 10
                result[p2] = total % 10

        start = 0
        while start < len(result) - 1 and result[start] == 0:
            start += 1

        return "".join(str(x) for x in result[start:])

if __name__ == "__main__":
    print(BigNumCalculator.add("12345678901234567890", "98765432109876543210"))
    print(BigNumCalculator.subtract("12345678901234567890", "98765432109876543210"))
    print(BigNumCalculator.multiply("12345678901234567890", "98765432109876543210"))