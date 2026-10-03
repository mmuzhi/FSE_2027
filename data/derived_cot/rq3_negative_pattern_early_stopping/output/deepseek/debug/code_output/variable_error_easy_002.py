from typing import List

class Solution:
    def findRestaurant(self, list1: List[str], list2: List[str]) -> List[str]:
        d2 = {}
        for i, s in enumerate(list2):
            d2[s] = i
        common = []
        for i, s in enumerate(list1):
            if s in d2:
                common.append([i + d2[s], s])
        if not common:
            return []
        common.sort()
        min_sum = common[0][0]
        result = [common[0][1]]
        for j in range(1, len(common)):
            if common[j][0] == min_sum:
                result.append(common[j][1])
            else:
                break
        return result