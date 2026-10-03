import bisect
from typing import List

class Solution:
    def medianSlidingWindow(self, nums: List[int], k: int) -> List[float]:
        win = []
        ans = []
        for i, x in enumerate(nums):
            if i >= k:
                # Remove the element that leaves
                pos = bisect.bisect_left(win, nums[i-k])
                win.pop(pos)
            bisect.insort(win, x)
            if len(win) == k:
                if k % 2 == 1:
                    ans.append(win[k//2])
                else:
                    ans.append((win[k//2-1] + win[k//2]) / 2)
        return ans