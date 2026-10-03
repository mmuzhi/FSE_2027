from typing import List

class Solution:
    def stoneGameVI(self, a: List[int], b: List[int]) -> int:
        combines = [(a[i] + b[i], a[i], b[i]) for i in range(len(a))]
        combines.sort(reverse=True)
        alicePoints = 0
        bobPoints = sum(b)
        for i in range(0, len(a), 2):
            alicePoints += combines[i][1]
            bobPoints -= combines[i][2]
        if alicePoints > bobPoints:
            return 1
        elif alicePoints < bobPoints:
            return -1
        else:
            return 0