from typing import List
from collections import defaultdict
import heapq

class Solution:
    def findMaximumElegance(self, items: List[List[int]], k: int) -> int:
        items.sort(key=lambda x: -x[0])
        
        heap = []
        cat_count = defaultdict(int)
        total = 0
        distinct = 0
        ans = 0
        
        for profit, category in items:
            heapq.heappush(heap, (profit, category))
            total += profit
            cat_count[category] += 1
            if cat_count[category] == 1:
                distinct += 1
            
            if len(heap) > k:
                removed_profit, removed_cat = heapq.heappop(heap)
                total -= removed_profit
                cat_count[removed_cat] -= 1
                if cat_count[removed_cat] == 0:
                    distinct -= 1
            
            if len(heap) == k:
                ans = max(ans, total + distinct * distinct)
        
        return ans