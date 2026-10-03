import heapq
from collections import defaultdict
from typing import List

class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)
        # The total length of segments is k * x, and the array length must be at least that.
        # We need to choose k non-overlapping segments of length x.
        # First, precompute the minimal cost for each window of length x.
        # Use two heaps: left_heap (max-heap) and right_heap (min-heap)
        left_heap = []
        right_heap = []
        left_freq = defaultdict(int)
        right_freq = defaultdict(int)
        left_sum = 0
        right_sum = 0
        count_left = (x + 1) // 2  # number of elements in left_heap

        # Function to add an element to the heaps
        def add_element(v):
            nonlocal left_sum, right_sum
            if left_heap and v <= -left_heap[0]:
                heapq.heappush(left_heap, -v)
                left_freq[v] += 1
                left_sum += v
            else:
                heapq.heappush(right_heap, v)
                right_freq[v] += 1
                right_sum += v

            # Balance the heaps
            if len(left_heap) > count_left:
                # Move the largest from left_heap to right_heap
                largest = -heapq.heappop(left_heap)
                left_freq[largest] -= 1
                if left_freq[largest] == 0:
                    del left_freq[largest]
                heapq.heappush(right_heap, largest)
                right_freq[largest] += 1
                right_sum += largest
            elif len(left_heap) < count_left:
                # Move the smallest from right_heap to left_heap
                smallest = heapq.heappop(right_heap)
                right_freq[smallest] -= 1
                if right_freq[smallest] == 0:
                    del right_freq[smallest]
                heapq.heappush(left_heap, -smallest)
                left_freq[smallest] += 1
                left_sum += smallest

        # Function to remove an element from the heaps
        def remove_element(v):
            nonlocal left_sum, right_sum
            if left_freq.get(v, 0) > 0:
                left_freq[v] -= 1
                left_sum -= v
                # If the top of left_heap is v and its frequency is 0, pop it
                if left_heap and -left_heap[0] == v and left_freq[v] == 0:
                    heapq.heappop(left_heap)
            else:
                right_freq[v] -= 1
                right_sum -= v
                if right_heap and right_heap[0] == v and right_freq[v] == 0:
                    heapq.heappop(right_heap)

        # First, build the window [0, x-1]
        for i in range(x):
            add_element(nums[i])
        
        # Function to get the minimal cost for the current window
        def get_cost():
            if not left_heap:
                return 0
            median = -left_heap[0]
            # The left part includes the median and the first count_left elements (smallest count_left elements)
            # The cost for the left part: (median - a) for each a in left_heap
            # But we have left_sum = sum of actual values in left_heap
            cost_left = count_left * median - left_sum
            cost_right = right_sum - (x - count_left) * median
            return cost_left + cost_right

        # Precompute min_cost for each window starting from 0 to n-x
        min_costs = [0] * (n - x + 1)
        min_costs[0] = get_cost()

        # Slide the window: remove nums[0] and add nums[x]
        for i in range(n - x):
            remove_element(nums[i])
            add_element(nums[i + x])
            min_costs[i + 1] = get_cost()

        # Now, we have min_costs[i] for each window starting at i.
        # Now, we need to choose k non-overlapping segments (each of length x) such that the sum of min_costs for these segments is minimized.
        # The segments cannot overlap, so the starting indices must be at least x apart (because a segment starting at i occupies [i, i+x-1], so the next must start at i+x or later).
        # We can use dynamic programming.
        # Let dp[j][i] = minimal total cost after choosing j segments and the last segment starts at i.
        # Then, dp[j][i] = min_costs[i] + min_{t from 0 to i-x} dp[j-1][t]
        # But i