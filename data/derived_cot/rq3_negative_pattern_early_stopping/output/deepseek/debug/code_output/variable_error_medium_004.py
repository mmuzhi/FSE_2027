from typing import List

class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        if len(prices) < 2:
            return 0
        profit = 0
        i = 0
        while i < len(prices) - 1:
            while i < len(prices) - 1 and prices[i] >= prices[i+1]:
                i += 1
            buy = prices[i]
            while i < len(prices) - 1 and prices[i] <= prices[i+1]:
                i += 1
            sell = prices[i]
            profit += sell - buy
        return profit