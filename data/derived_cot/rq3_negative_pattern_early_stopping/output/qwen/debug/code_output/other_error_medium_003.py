class Solution:
    def getMaximumConsecutive(self, coins: List[int]) -> int:
        coins.sort()
        current = 1
        for c in coins:
            if c > current:
                break
            current += c
        return current
