import bisect

class Solution:
    def medianSlidingWindow(self, nums: List[int], k: int) -> List[float]:
        window = []
        ans = []
        for i, x in enumerate(nums):
            bisect.insort(window, x)
            if i >= k:
                window.remove(nums[i - k + 1])
            if len(window) == k:
                if k % 2 == 1:
                    ans.append(window[k//2])
                else:
                    ans.append((window[k//2 - 1] + window[k//2]) / 2)
        return ans