from typing import List

class Solution:
    def numberOfGoodSubarraySplits(self, nums: List[int]) -> int:
        MOD = 1000000007
        ans = 1
        prev = -1

        for i, num in enumerate(nums):
            if num == 1:
                if prev != -1:
                    ans = (ans * (i - prev)) % MOD
                prev = i

        return 0 if prev == -1 else ans