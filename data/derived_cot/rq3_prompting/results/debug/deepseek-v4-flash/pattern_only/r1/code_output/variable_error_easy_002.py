from typing import List

class Solution:
    def findRestaurant(self, list1: List[str], list2: List[str]) -> List[str]:
        index_by_name = {name: i for i, name in enumerate(list2)}
        min_sum = float('inf')
        ans = []

        for i, name in enumerate(list1):
            if name in index_by_name:
                total = i + index_by_name[name]

                if total < min_sum:
                    min_sum = total
                    ans = [name]
                elif total == min_sum:
                    ans.append(name)

        return ans