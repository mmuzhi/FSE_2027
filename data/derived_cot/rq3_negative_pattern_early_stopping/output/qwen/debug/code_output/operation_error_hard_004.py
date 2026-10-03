import math
from typing import List
import bisect

class Solution:
    def maximumSumQueries(self, nums1: List[int], nums2: List[int], queries: List[List[int]]) -> List[int]:
        n = len(nums1)
        a = sorted(zip(nums1, nums2))
        # Precompute max_y: the maximum nums2 from index i to the end
        max_y = [0] * n
        max_val = -1
        for i in range(n-1, -1, -1):
            if a[i][1] > max_val:
                max_val = a[i][1]
            max_y[i] = max_val
        
        # Build sparse table for _sum = nums1[i] + nums2[i]
        k = int(math.log2(n)) + 1
        st = [[0] * n for _ in range(k)]
        # Base case: st[0][i] = a[i][0] + a[i][1]
        for i in range(n):
            st[0][i] = a[i][0] + a[i][1]
        
        # Build the sparse table
        for i in range(1, k):
            j = 0
            while j + (1 << i) <= n:
                st[i][j] = max(st[i-1][j], st[i-1][j + (1 << (i-1))])
                j += 1
        
        def query_max(l, r):
            if l > r:
                return -10**18
            length = r - l + 1
            k = math.floor(math.log2(length))
            return max(st[k][l], st[k][r - (1 << k) + 1])
        
        res = []
        for x, y in queries:
            # Find the first index where a[i][0] >= x and a[i][1] >= y
            # Since a is sorted by nums1 and then nums2, we can use bisect
            i = bisect.bisect_left(a, (x, y))
            if i == n or max_y[i] < y:
                res.append(-1)
                continue
            
            # Now, we need to find the largest index j such that from i to j, there is at least one point with nums2>=y
            # But note: we already know that from i to the end, the maximum nums2 is max_y[i] which is >= y.
            # However, we need to find the range of indices that have at least one point with nums2>=y, but note that the condition is on the point's nums2.
            # We are going to find the last index j such that the maximum nums2 from j to the end is >= y.
            # But note: we have max_y array which is the suffix maximum of nums2. We want the largest index j such that max_y[j] >= y.
            # We can do a binary search on the max_y array from index i to n-1.
            left, right = i, n-1
            ans_index = i
            while left <= right:
                mid = (left + right) // 2
                if max_y[mid] >= y:
                    ans_index = mid
                    left = mid + 1
                else:
                    right = mid - 1
            
            # Now, we have the range [i, ans_index] (which is the set of points that are >= (x, y) and have at least one point with nums2>=y)
            # But note: the entire range [i, ans_index] might not have every point with nums2>=y, but we are only concerned with the maximum sum in the entire range [i, ans_index] (which is the set of points that are >= (x, y) and have at least one point with nums2>=y). However, note that the condition for the query is that the point must have nums1>=x and nums2>=y. The points in [i, ans_index] are >= (x, y) in the sorted order (so nums1>=x) and we have ensured that there is at least one point with nums2>=y. But note: the point at index i might have nums2<y, but then we have a later point with nums2>=y. However, the query requires that the point has both conditions. We are allowed to use any point in the range [i, ans_index] that has nums2>=y. But note: the condition for the query is that the point must have both. The sorted array and the max_y array do not guarantee that every point in [i, ans_index] has nums2>=y. We only know that the maximum nums2 from i to ans_index is >= y. But note: the condition for the