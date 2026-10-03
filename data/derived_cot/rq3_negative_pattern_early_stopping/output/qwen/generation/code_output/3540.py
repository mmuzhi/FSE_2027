class Solution:
    def stringHash(self, s: str, k: int) -> str:
        n = len(s)
        result = []
        for i in range(0, n, k):
            total = 0
            for char in s[i:i+k]:
                total += ord(char) - ord('a')
            hashed_char = total % 26
            result.append(chr(hashed_char + ord('a')))
        return ''.join(result)