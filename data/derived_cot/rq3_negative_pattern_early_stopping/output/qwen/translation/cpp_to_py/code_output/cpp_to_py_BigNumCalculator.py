class BigNumCalculator:
    @staticmethod
    def add(num1, num2):
        max_len = max(len(num1), len(num2))
        num1_padded = num1.zfill(max_len)
        num2_padded = num2.zfill(max_len)
        
        carry = 0
        result = []
        for i in range(max_len-1, -1, -1):
            digit_sum = int(num1_padded[i]) + int(num2_padded[i]) + carry
            carry = digit_sum // 10
            digit = digit_sum % 10
            result.insert(0, str(digit))
        
        if carry:
            result.insert(0, str(carry))
        return ''.join(result)

    @staticmethod
    def subtract(num1, num2):
        if num1 == num2:
            return "0"
        if num1.startswith('-') or num2.startswith('-'):
            raise ValueError("Negative numbers are not supported in subtraction")
        
        num1, num2 = num1.lstrip('-'), num2.lstrip('-')
        if len(num1) < len(num2) or (len(num1) == len(num2) and num1 < num2):
            num1, num2 = num2, num1
            negative = True
        else:
            negative = False
        
        max_len = max(len(num1), len(num2))
        num1 = num1.zfill(max_len)
        num2 = num2.zfill(max_len)
        
        borrow = 0
        result = []
        for i in range(max_len-1, -1, -1):
            digit_diff = int(num1[i]) - int(num2[i]) - borrow
            if digit_diff < 0:
                digit_diff += 10
                borrow = 1
            else:
                borrow = 0
            result.insert(0, str(digit_diff))
        
        result_str = ''.join(result).lstrip('0')
        if not result_str:
            result_str = "0"
        if negative:
            result_str = '-' + result_str
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
                total = mul + result[i+j+1]
                carry = total // 10
                result[i+j+1] = total % 10
                result[i+j] += carry
        
        result_str = ''.join(str(d) for d in result if d != 0)
        if not result_str:
            return "0"
        return result_str