from typing import List
import heapq

class Solution:
    def medianSlidingWindow(self, nums: List[int], k: int) -> List[float]:
        lo = []  # max heap: (-value, -index)
        hi = []  # min heap: (value, index)
        belongs = {}
        removed = set()
        lo_size = 0
        hi_size = 0

        def clean() -> None:
            while lo and -lo[0][1] in removed:
                heapq.heappop(lo)
            while hi and hi[0][1] in removed:
                heapq.heappop(hi)

        def rebalance() -> None:
            nonlocal lo_size, hi_size
            while lo_size > hi_size + 1:
                clean()
                neg_val, neg_idx = heapq.heappop(lo)
                val = -neg_val
                idx = -neg_idx
                lo_size -= 1
                heapq.heappush(hi, (val, idx))
                belongs[idx] = 1
                hi_size += 1
            while hi_size > lo_size:
                clean()
                val, idx = heapq.heappop(hi)
                hi_size -= 1
                heapq.heappush(lo, (-val, -idx))
                belongs[idx] = 0
                lo_size += 1

        def add(x: int, idx: int) -> None:
            nonlocal lo_size, hi_size
            clean()
            if not lo or x <= -lo[0][0]:
                heapq.heappush(lo, (-x, -idx))
                belongs[idx] = 0
                lo_size += 1
            else:
                heapq.heappush(hi, (x, idx))
                belongs[idx] = 1
                hi_size += 1
            rebalance()

        def remove(idx: int) -> None:
            nonlocal lo_size, hi_size
            clean()
            if belongs[idx] == 0:
                lo_size -= 1
            else:
                hi_size -= 1
            removed.add(idx)
            belongs.pop(idx, None)
            clean()
            rebalance()

        ans = []
        for i, x in enumerate(nums):
            add(x, i)
            if i >= k:
                remove(i - k)
            if i >= k - 1:
                clean()
                if k % 2 == 1:
                    ans.append(float(-lo[0][0]))
                else:
                    ans.append((-lo[0][0] + hi[0][0]) / 2.0)
        return ans