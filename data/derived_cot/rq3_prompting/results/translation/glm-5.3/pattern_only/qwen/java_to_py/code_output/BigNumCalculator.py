def add(num1: str, num2: str) -> str:
    max_length = max(len(num1), len(num2))
    # Mirrors String.format("%Ns", s).replace(' ', '0')
    num1 = num1.rjust(max_length).replace(' ', '0')
    num2 = num2.rjust(max_length).replace(' ', '0')

    carry = 0
    result = []
    for i in range(max_length - 1, -1, -1):
        digit_sum = int(num1[i]) + int(num2[i]) + carry
        carry = digit_sum // 10
        digit = digit_sum % 10
        result.append(str(digit))

    if carry > 0:
        result.append(str(carry))

    return ''.join(reversed(result))


def subtract(num1: str, num2: str) -> str:
    negative = False
    if len(num1) < len(num2) or (len(num1) == len(num2) and num1 < num2):
        num1, num2 = num2, num1
        negative = True

    max_length = max(len(num1), len(num2))
    num1 = num1.rjust(max_length).replace(' ', '0')
    num2 = num2.rjust(max_length).replace(' ', '0')

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

    s = ''.join(reversed(result))

    # Strip leading zeros, keep at least one digit (Java: while len>1 and head=='0')
    start = 0
    while len(s) - start > 1 and s[start] == '0':
        start += 1
    s = s[start:]

    if negative:
        s = '-' + s

    return s


def multiply(num1: str, num2: str) -> str:
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

    return ''.join(str(d) for d in result[start:])


if __name__ == "__main__":
    print(add("12345678901234567890", "98765432109876543210"))
    print(subtract("12345678901234567890", "98765432109876543210"))
    print(multiply("12345678901234567890", "98765432109876543210"))