import bisect

class Solution:
    def medianSlidingWindow(self, nums: List[int], k: int) -> List[float]:
        sorted_list = []
        ans = []
        for i, x in enumerate(nums):
            bisect.insort(sorted_list, x)
            if i >= k:
                # Remove the element that is leaving (the one at index i-k in the original array)
                # Use bisect to find the first occurrence of the element to remove
                pos = bisect.bisect_left(sorted_list, nums[i-k])
                del sorted_list[pos]
            if i >= k-1:
                if k % 2 == 1:
                    ans.append(sorted_list[k//2])
                else:
                    ans.append((sorted_list[k//2-1] + sorted_list[k//2]) /  2)
        return ans