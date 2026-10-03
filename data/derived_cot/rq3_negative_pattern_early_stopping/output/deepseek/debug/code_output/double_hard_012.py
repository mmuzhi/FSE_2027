from typing import List
import heapq
import collections

class Solution:
    def medianSlidingWindow(self, nums: List[int], k: int) -> List[float]:
        left = []  # max heap (store negative values)
        right = [] # min heap
        to_remove = collections.defaultdict(int)
        
        def add(num: int) -> None:
            if not left or num <= -left[0]:
                heapq.heappush(left, -num)
            else:
                heapq.heappush(right, num)
            if len(left) > len(right) + 1:
                heapq.heappush(right, -heapq.heappop(left))
            elif len(right) > len(left):
                heapq.heappush(left, -heapq.heappop(right))
        
        def remove(num: int) -> None:
            to_remove[num] += 1
        
        def prune() -> None:
            while left and to_remove[-left[0]] > 0:
                to_remove[-left[0]] -= 1
                heapq.heappop(left)
            while right and to_remove[right[0]] > 0:
                to_remove[right[0]] -= 1
                heapq.heappop(right)
        
        def get_median() -> float:
            prune()
            if k % 2 == 1:
                return -left[0]
            else:
                return (-left[0] + right[0]) / 2.0
        
        ans = []
        for i, num in enumerate(nums):
            add(num)
            if i >= k:
                remove(nums[i - k])
            if i >= k - 1:
                prune()
                while len(left) > len(right) + 1:
                    heapq.heappush(right, -heapq.heappop(left))
                while len(right) > len(left):
                    heapq.heappush(left, -heapq.heappop(right))
                ans.append(get_median())
        return ans