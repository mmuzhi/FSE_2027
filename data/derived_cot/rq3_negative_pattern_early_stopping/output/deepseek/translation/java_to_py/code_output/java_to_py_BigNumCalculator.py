def add(num1: str, num2: str) -> str:
    max_len = max(len(num1), len(num2))
    num1 = num1.rjust(max_len, '0')
    num2 = num2.rjust(max_len, '0')
    carry = 0
    result = []
    for i in range(max_len - 1, -1, -1):
        digit_sum = int(num1[i]) + int(num2[i]) + carry
        carry = digit_sum // 10
        digit = digit_sum % 10
        result.insert(0, str(digit))
    if carry:
        result.insert(0, str(carry))
    return ''.join(result)

def subtract(num1: str, num2: str) -> str:
    negative = False
    if len(num1) < len(num2) or (len(num1) == len(num2) and num1 < num2):
        num1, num2 = num2, num1
        negative = True
    max_len = max(len(num1), len(num2))
    num1 = num1.rjust(max_len, '0')
    num2 = num2.rjust(max_len, '0')
    borrow = 0
    result = []
    for i in range(max_len - 1, -1, -1):
        digit_diff = int(num1[i]) - int(num2[i]) - borrow
        if digit_diff < 0:
            digit_diff += 10
            borrow = 1
        else:
            borrow = 0
        result.insert(0, str(digit_diff))
    while len(result) > 1 and result[0] == '0':
        result.pop(0)
    if negative:
        result.insert(0, '-')
    return ''.join(result)

def multiply(num1: str, num2: str) -> str:
    len1, len2 = len(num1), len(num2)
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
    return ''.join(str(d) for d in result[start:])

if __name__ == '__main__':
    print(add("12345678901234567890", "98765432109876543210"))
    print(subtract("12345678901234567890", "98765432109876543210"))
    print(multiply("12345678901234567890", "98765432109876543210"))