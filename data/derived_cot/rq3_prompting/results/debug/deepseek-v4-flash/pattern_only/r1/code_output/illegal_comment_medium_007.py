class Solution:
    def minimumPartition(self, s: str, k: int) -> int:
        ans = 1
        curr = 0

        for d in s:
            val = int(d)
            if val > k:
                return -1

            curr = curr * 10 + val
            if curr > k:
                ans += 1
                curr = val

        return ans