from typing import List
from collections import Counter

class Solution:
    def minimumTotalCost(self, nums1: List[int], nums2: List[int]) -> int:
        n = len(nums1)
        ans = 0
        cnt = Counter()

        for i in range(n):
            if nums1[i] == nums2[i]:
                cnt[nums1[i]] += 1
                ans += i

        if not cnt:
            return 0

        max_val = max(cnt, key=cnt.get)
        max_cnt = cnt[max_val]
        rest = sum(cnt.values()) - max_cnt

        if rest >= max_cnt:
            return ans

        need = max_cnt - rest

        for i in range(n):
            if need == 0:
                return ans
            a, b = nums1[i], nums2[i]
            if a != b and a != max_val and b != max_val:
                ans += i
                need -= 1

        return -1