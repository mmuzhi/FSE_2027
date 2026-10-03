from typing import List
import heapq

class Solution:
    def medianSlidingWindow(self, nums: List[int], k: int) -> List[float]:
        lo = []   # max-heap (store -value)
        hi = []   # min-heap
        ans = []
        to_remove = {}
        
        def balance():
            while len(lo) > len(hi) + 1:
                heapq.heappush(hi, -heapq.heappop(lo))
            while len(hi) > len(lo):
                heapq.heappush(lo, -heapq.heappop(hi))
        
        def add(num):
            if not lo or num <= -lo[0]:
                heapq.heappush(lo, -num)
            else:
                heapq.heappush(hi, num)
            balance()
        
        def remove(num):
            to_remove[num] = to_remove.get(num, 0) + 1
            pass
        
        
        import bisect
        window = sorted(nums[:k])
        if k % 2 == 1:
            ans.append(float(window[k//2]))
        else:
            ans.append((window[k//2-1] + window[k//2]) / 2.0)
        
        for i in range(k, len(nums)):
            left = nums[i-k]
            idx = bisect.bisect_left(window, left)
            window.pop(idx)
            bisect.insort(window, nums[i])
            if k % 2 == 1:
                ans.append(float(window[k//2]))
            else:
                ans.append((window[k//2-1] + window[k//2]) / 2.0)
        
        return ans