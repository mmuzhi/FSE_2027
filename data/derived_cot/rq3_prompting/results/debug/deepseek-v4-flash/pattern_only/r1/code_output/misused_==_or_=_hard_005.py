from typing import List
from collections import Counter

class Solution:
    def minimumTotalCost(self, nums1: List[int], nums2: List[int]) -> int:
        cnt = Counter()
        ans = 0

        for i, (a, b) in enumerate(zip(nums1, nums2)):
            if a == b:
                cnt[a] += 1
                ans += i

        if not cnt:
            return 0

        total = sum(cnt.values())
        max_freq = max(cnt.values())
        max_val = max(cnt, key=cnt.get)

        if max_freq <= total - max_freq:
            return ans

        need = max_freq - (total - max_freq)

        for i, (a, b) in enumerate(zip(nums1, nums2)):
            if need == 0:
                break
            if a != b and a != max_val and b != max_val:
                ans += i
                need -= 1

        return -1 if need else ans