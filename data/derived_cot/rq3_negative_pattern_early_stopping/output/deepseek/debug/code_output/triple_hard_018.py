from typing import List
import bisect

class Solution:
    def medianSlidingWindow(self, nums: List[int], k: int) -> List[float]:
        window = []
        ans = []
        for i, x in enumerate(nums):
            bisect.insort(window, x)
            if len(window) > k:
                left = nums[i - k]
                idx = bisect.bisect_left(window, left)
                window.pop(idx)
            if len(window) == k:
                if k % 2 == 1:
                    ans.append(float(window[k // 2]))
                else:
                    ans.append((window[k // 2 - 1] + window[k // 2]) / 2.0)
        return ans