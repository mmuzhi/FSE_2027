class Solution:
    def numOfPairs(self, nums: List[str], target: str) -> int:
        from collections import defaultdict
        d = defaultdict(int)
        for num_str in nums:
            d[num_str] += 1
            
        n = len(target)
        pairs = 0
        
        # Consider every possible split of the target string
        for i in range(1, n):
            part1 = target[:i]
            part2 = target[i:]
            if part1 in d and part2 in d:
                pairs += d[part1] * d[part2]
                
        return pairs