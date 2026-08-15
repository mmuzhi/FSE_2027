from typing import List

class Solution:
    def findRestaurant(self, list1: List[str], list2: List[str]) -> List[str]:
        d2 = {}
        for i, restaurant in enumerate(list2):
            d2[restaurant] = i

        pairs = []
        for i, restaurant in enumerate(list1):
            if restaurant in d2:
                pairs.append([i + d2[restaurant], restaurant])

        if not pairs:
            return []

        pairs.sort()
        min_sum = pairs[0][0]
        return [restaurant for s, restaurant in pairs if s == min_sum]