from typing import List

class Solution:
    def findRestaurant(self, list1: List[str], list2: List[str]) -> List[str]:
        d2 = {s: i for i, s in enumerate(list2)}
        candidates = []

        for i, s in enumerate(list1):
            if s in d2:
                candidates.append([i + d2[s], s])

        if not candidates:
            return []

        candidates.sort()
        min_sum = candidates[0][0]

        return [s for total, s in candidates if total == min_sum]