class Solution:
    def minimumPartition(self, s: str, k: int) -> int:
        ans = 1
        curr = 0
        for d in s:
            digit = int(d)
            if digit > k:
                return -1
            curr = 10 * curr + digit
            if curr > k:
                ans += 1
                curr = digit
        return ans