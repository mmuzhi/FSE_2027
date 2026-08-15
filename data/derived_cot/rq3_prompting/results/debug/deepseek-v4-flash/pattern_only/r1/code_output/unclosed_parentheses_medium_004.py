from collections import Counter
from typing import List

class Solution:
    def numOfPairs(self, nums: List[str], target: str) -> int:
        cnt = Counter(nums)
        ans = 0

        for i in range(len(target) + 1):
            prefix = target[:i]
            suffix = target[i:]

            if prefix == suffix:
                ans += cnt[prefix] * (cnt[prefix] - 1)
            else:
                ans += cnt[prefix] * cnt[suffix]

        return ans