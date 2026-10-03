class Solution:
    def findLHS(self, nums: List[int]) -> int:
        from collections import defaultdict
        count_map = defaultdict(int)
        for num in nums:
            count_map[num] += 1
        
        result = 0
        for num in count_map:
            if num + 1 in count_map:
                result = max(result, count_map[num] + count_map[num+1])
        return result
