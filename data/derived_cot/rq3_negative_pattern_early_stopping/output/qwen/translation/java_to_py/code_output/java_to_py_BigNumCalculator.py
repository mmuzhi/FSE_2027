class BigNumCalculator:

    @staticmethod
    def add(num1, num2):
        len1 = len(num1)
        len2 = len(num2)
        max_len = max(len1, len2)
        num1 = num1.zfill(max_len)
        num2 = num2.zfill(max_len)
        carry = 0
        result = []
        for i in range(max_len-1, -1, -1):
            digit_sum = int(num1[i]) + int(num2[i]) + carry
            carry = digit_sum // 10
            result.append(str(digit_sum % 10))
        if carry:
            result.append(str(carry))
        return ''.join(result[::-1])

    @staticmethod
    def subtract(num1, num2):
        if num1 == num2:
            return "0"
        if num1 < num2:
            return '-' + BigNumCalculator.subtract(num2, num1)
        len1 = len(num1)
        len2 = len(num2)
        max_len = max(len1, len2)
        num1 = num1.zfill(max_len)
        num2 = num2.zfill(max_len)
        borrow = 0
        result = []
        for i in range(max_len-1, -1, -1):
            diff = int(num1[i]) - int(num2[i]) - borrow
            if diff < 0:
                diff += 10
                borrow = 1
            else:
                borrow = 0
            result.append(str(diff))
        # Remove leading zeros
        result_str = ''.join(result[::-1]).lstrip('0')
        if not result_str:
            return "0"
        if result_str.startswith('-'):
            return result_str
        return result_str

    @staticmethod
    def multiply(num1, num2):
        if num1 == "0" or num2 == "0":
            return "0"
        len1 = len(num1)
        len2 = len(num2)
        result = [0] * (len1 + len2)
        for i in range(len1-1, -1, -1):
            for j in range(len2-1, -1, -1):
                mul = int(num1[i]) * int(num2[j])
                p1 = i + j
                p2 = i + j + 1
                total = mul + result[p2]
                result[p1] += total // 10
                result[p2] = total % 10
        # Remove leading zeros
        result_str = ''.join(str(d) for d in result if d != 0)
        return result_str if result_str else "0"

    @staticmethod
    def main():
        print(BigNumCalculator.add("12345678901234567890", "98765432109876543210"))
        print(BigNumCalculator.subtract("12345678901234567890", "98765432109876543210"))
        print(BigNumCalculator.multiply("12345678901234567890", "98765432109876543210"))

if __name__ == "__main__":
    BigNumCalculator.main()