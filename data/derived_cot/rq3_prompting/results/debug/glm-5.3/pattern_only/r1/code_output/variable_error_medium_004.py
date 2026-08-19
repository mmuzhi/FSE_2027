class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        if len(prices) < 2:
            return 0
        if len(prices) == 2:
            output = prices[1] - prices[0]
            return output if output > 0 else 0
        i = 0
        j = 1
        stockBuy = prices[i]
        stockSell = prices[j]
        counter = 0
        profit = 0
        while counter < len(prices) - 2:
            if stockSell - stockBuy < 0:
                i = j
                j = i + 1
            else:
                if j + 1 < len(prices) and prices[j + 1] > prices[j]:
                    j += 1
                else:
                    profit = profit + (stockSell - stockBuy)
                    i = j + 1
                    j = i + 1
            if j >= len(prices):
                break
            stockSell = prices[j]
            stockBuy = prices[i]
            counter += 1
        if j < len(prices) and prices[j] - prices[i] > 0:
            profit = profit + (prices[j] - prices[i])
        return profit