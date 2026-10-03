class Solution:
    def stoneGameVI(self, a: List[int], b: List[int]) -> int:
        combines = [(a[i] + b[i], a[i], b[i]) for i in range(len(a))]
        combines.sort(reverse=True)
        alicePoints = sum(combines[i][1] for i in range(0, len(a), 2))
        bobPoints = sum(combines[i][2] for i in range(1, len(a), 2))
        if alicePoints > bobPoints:
            return 1
        elif alicePoints < bobPoints:
            return -1
        return 0