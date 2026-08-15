from typing import List
import heapq

class Solution:
    def medianSlidingWindow(self, nums: List[int], k: int) -> List[float]:
        small = []
        large = []
        removed = [False] * len(nums)
        heap_of = [0] * len(nums)
        small_cnt = 0
        large_cnt = 0
        ans = []

        def clean_small():
            while small and removed[small[0][1]]:
                heapq.heappop(small)

        def clean_large():
            while large and removed[large[0][1]]:
                heapq.heappop(large)

        def rebalance():
            nonlocal small_cnt, large_cnt

            while small_cnt > large_cnt + 1:
                clean_small()
                neg_v, idx = heapq.heappop(small)
                small_cnt -= 1
                heapq.heappush(large, (-neg_v, idx))
                heap_of[idx] = 1
                large_cnt += 1

            while large_cnt > small_cnt:
                clean_large()
                v, idx = heapq.heappop(large)
                large_cnt -= 1
                heapq.heappush(small, (-v, idx))
                heap_of[idx] = 0
                small_cnt += 1

        for i, x in enumerate(nums):
            clean_small()
            clean_large()

            if not small or x <= -small[0][0]:
                heapq.heappush(small, (-x, i))
                small_cnt += 1
                heap_of[i] = 0
            else:
                heapq.heappush(large, (x, i))
                large_cnt += 1
                heap_of[i] = 1

            rebalance()

            if i >= k:
                idx = i - k
                removed[idx] = True
                if heap_of[idx] == 0:
                    small_cnt -= 1
                else:
                    large_cnt -= 1
                rebalance()

            if i >= k - 1:
                clean_small()
                clean_large()

                if k % 2 == 1:
                    ans.append(float(-small[0][0]))
                else:
                    ans.append((-small[0][0] + large[0][0]) / 2.0)

        return ans