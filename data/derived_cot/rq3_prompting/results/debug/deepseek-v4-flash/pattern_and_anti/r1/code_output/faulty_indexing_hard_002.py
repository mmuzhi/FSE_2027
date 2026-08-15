from typing import List
import heapq

class Solution:
    def findMaximumElegance(self, items: List[List[int]], k: int) -> int:
        items.sort(key=lambda x: x[0], reverse=True)

        total = 0
        seen = set()
        duplicate_profits = []

        for profit, category in items[:k]:
            total += profit
            if category in seen:
                heapq.heappush(duplicate_profits, profit)
            else:
                seen.add(category)

        ans = total + len(seen) * len(seen)

        for profit, category in items[k:]:
            if category in seen:
                continue
            if not duplicate_profits:
                break

            total += profit - heapq.heappop(duplicate_profits)
            seen.add(category)
            ans = max(ans, total + len(seen) * len(seen))

        return ans