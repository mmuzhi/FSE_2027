from typing import List

class Solution:
    def minOperationsMaxProfit(self, customers: List[int], boardingCost: int, runningCost: int) -> int:
        max_profit = -1
        ans = 0
        cur_customers = 0
        wait = 0
        rotations = 0
        i = 0
        n = len(customers)
        
        while i < n or wait > 0:
            if i < n:
                wait += customers[i]
                i += 1
            
            rotations += 1
            board = min(4, wait)
            wait -= board
            cur_customers += board
            profit = cur_customers * boardingCost - rotations * runningCost
            
            if profit > max_profit:
                max_profit = profit
                ans = rotations
        
        return -1 if max_profit <= 0 else ans