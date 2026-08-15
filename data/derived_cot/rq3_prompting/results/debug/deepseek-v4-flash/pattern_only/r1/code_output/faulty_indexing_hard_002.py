from typing import List
import heapq

class Solution:
    def findMaximumElegance(self, items: List[List[int]], k: int) -> int:
        items.sort(key=lambda x: x[0], reverse=True)

        total = 0
        categories = set()
        duplicates = []

        for i in range(k):
            profit, category = items[i]
            total += profit
            if category in categories:
                heapq.heappush(duplicates, profit)
            else:
                categories.add(category)

        ans = total + len(categories) * len(categories)

        for i in range(k, len(items)):
            profit, category = items[i]
            if category not in categories and duplicates:
                total += profit - heapq.heappop(duplicates)
                categories.add(category)
                ans = max(ans, total + len(categories) * len(categories))

        return ans