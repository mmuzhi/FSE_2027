import bisect
from typing import List

class Solution:
    def medianSlidingWindow(self, nums: List[int], k: int) -> List[float]:
        window = []
        ans = []
        for i, x in enumerate(nums):
            bisect.insort(window, x)
            if len(window) > k:
                window.pop(bisect.bisect_left(window, nums[i - k]))
            if len(window) == k:
                if k % 2 == 1:
                    ans.append(window[k // 2])
                else:
                    ans.append((window[k // 2 - 1] + window[k // 2]) / 2)
        return ans