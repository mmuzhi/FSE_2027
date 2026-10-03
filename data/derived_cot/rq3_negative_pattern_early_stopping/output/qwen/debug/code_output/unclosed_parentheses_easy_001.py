class Solution:
    def largestInteger(self, num: int) -> int:
        s = str(num)
        even_indices = []
        odd_indices = []
        for i, char in enumerate(s):
            digit = int(char)
            if i % 2 == 0:
                even_indices.append(digit)
            else:
                odd_indices.append(digit)
        even_indices.sort(reverse=True)
        odd_indices.sort(reverse=True)
        result = []
        for i in range(len(s)):
            if i % 2 == 0:
                result.append(str(even_indices.pop(0)))
            else:
                result.append(str(odd_indices.pop(0)))
        return int(''.join(result))
