from collections import defaultdict
from typing import List


class Solution:
    def findMaximumElegance(self, items: List[List[int]], k: int) -> int:
        dico = defaultdict(list)
        for profit, category in items:
            dico[category].append(profit)
        categories = []
        for category in dico:
            categories.append(sorted(dico[category]))
        categories.sort(key=lambda x: x[-1], reverse=True)

        def elegance(distinct):
            res = 0
            rest = []
            for i in range(distinct):
                res += categories[i][-1]
                for j in range(len(categories[i]) - 1):
                    rest.append(categories[i][j])
            rest.sort(reverse=True)
            if len(rest) < k - distinct:
                return -1
            return res + sum(rest[:k - distinct]) + distinct ** 2

        best = -1
        for d in range(1, min(len(categories), k) + 1):
            best = max(best, elegance(d))
        return best