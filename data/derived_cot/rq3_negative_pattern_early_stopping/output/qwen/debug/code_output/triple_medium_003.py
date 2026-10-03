class Solution:
    def moveStonesII(self, stones: List[int]) -> List[int]:
        stones.sort()
        n = len(stones)
        if n == 0:
            return [0, 0]
        max_consecutive = 1
        current = 1
        for i in range(1, n):
            if stones[i] == stones[i-1] + 1:
                current += 1
            else:
                if current > max_consecutive:
                    max_consecutive = current
                current = 1
        if current > max_consecutive:
            max_consecutive = current
        
        min_stones = 1
        max_stones = max_consecutive
        
        return [min_stones, max_stones]
