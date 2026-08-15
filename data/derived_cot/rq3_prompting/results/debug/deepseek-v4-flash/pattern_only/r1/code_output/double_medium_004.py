from collections import defaultdict
from typing import List

class Solution:
    def findWinners(self, matches: List[List[int]]) -> List[List[int]]:
        winners = defaultdict(int)
        losers = defaultdict(int)

        for match in matches:
            winner, loser = match[0], match[1]
            winners[winner] += 1
            losers[loser] += 1

        res_1, res_2 = [], []

        for k in winners:
            if k not in losers:
                res_1.append(k)

        for k, v in losers.items():
            if v == 1:
                res_2.append(k)

        res_1.sort()
        res_2.sort()

        return [res_1, res_2]