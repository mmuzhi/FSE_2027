from typing import List

class Solution:
    def answerQueries(self, nums: List[int], queries: List[int]) -> List[int]:
        nums.sort()
        sums = [0]
        for num in nums:
            sums.append(sums[-1] + num)
        
        def bSearch(q: int) -> int:
            l, r = 0, len(sums) - 1
            while l <= r:
                mid = (l + r) // 2
                if sums[mid] <= q:
                    l = mid + 1
                else:
                    r = mid - 1
            return r  # largest index with sums[r] <= q
        
        return [bSearch(q) for q in queries]