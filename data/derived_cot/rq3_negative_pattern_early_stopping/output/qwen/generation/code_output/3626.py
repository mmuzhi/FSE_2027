class Solution:
    def smallestNumber(self, n: int, t: int) -> int:
        if t == 1:
            return n
        num = n
        while True:
            # Calculate the product of digits
            product = 1
            for digit in str(num):
                product *= int(digit)
            if product % t == 0:
                return num
            num += 1