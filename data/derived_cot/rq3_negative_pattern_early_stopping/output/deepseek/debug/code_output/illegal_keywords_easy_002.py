from typing import List

class Solution:
    def findRestaurant(self, list1: List[str], list2: List[str]) -> List[str]:
        d2 = {}
        for i, val in enumerate(list2):
            d2[val] = i

        common = []
        for i, val in enumerate(list1):
            if val in d2:
                common.append((i + d2[val], val))

        if not common:
            return []

        common.sort()
        min_sum = common[0][0]
        result = [common[0][1]]
        for i in range(1, len(common)):
            if common[i][0] == min_sum:
                result.append(common[i][1])
            else:
                break
        return result