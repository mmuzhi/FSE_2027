class Solution:
    def stoneGameVI(self, a: List[int], b: List[int]) -> int:
        a.sort(reverse=True)
        b.sort(reverse=True)
        alice = 0
        bob = 0
        n = len(a)
        for i in range(n):
            if i % 2 == 0:
                alice += a[i]
            else:
                bob += b[i]
        if alice > bob:
            return 1
        elif alice < bob:
            return -1
        else:
            return 0