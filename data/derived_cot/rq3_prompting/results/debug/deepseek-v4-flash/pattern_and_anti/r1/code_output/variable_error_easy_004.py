from typing import List

class Solution:
    def answerQueries(self, nums: List[int], queries: List[int]) -> List[int]:
        nums.sort()
        prefix = [0]
        for num in nums:
            prefix.append(prefix[-1] + num)

        def bSearch(q: int) -> int:
            l, r = 0, len(prefix)
            while l < r:
                mid = (l + r) // 2
                if prefix[mid] <= q:
                    l = mid + 1
                else:
                    r = mid
            return l - 1

        return [bSearch(q) for q in queries]