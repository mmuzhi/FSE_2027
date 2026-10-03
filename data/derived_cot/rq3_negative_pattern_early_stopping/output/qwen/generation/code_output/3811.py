class Solution:
    def reverseDegree(self, s: str) -> int:
        total = 0
        for idx, char in enumerate(s):
            reversed_index = 26 - (ord(char) - ord('a'))
            total += reversed_index * (idx + 1)
        return total