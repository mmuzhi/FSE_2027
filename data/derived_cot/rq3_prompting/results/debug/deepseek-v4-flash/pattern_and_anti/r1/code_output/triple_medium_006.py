from typing import List

class Solution:
    def stoneGameVI(self, a: List[int], b: List[int]) -> int:
        stones = [(a[i] + b[i], a[i], b[i]) for i in range(len(a))]
        stones.sort(reverse=True)

        alice = 0
        bob = 0

        for i, (_, av, bv) in enumerate(stones):
            if i % 2 == 0:
                alice += av
            else:
                bob += bv

        if alice > bob:
            return 1
        if alice < bob:
            return -1
        return 0