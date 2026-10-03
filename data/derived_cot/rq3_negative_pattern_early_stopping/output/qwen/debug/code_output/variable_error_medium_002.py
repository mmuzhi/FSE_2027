class Solution:
    def stoneGameVI(self, a: List[int], b: List[int]) -> int:
        # Combine all stones and sort in descending order
        stones = a + b
        stones.sort(reverse=True)
        aliceScore = 0
        bobScore = 0
        # Alice starts first, so she takes the stones at indices 0, 2, 4, ... (even indices in 0-indexed)
        for i in range(len(stones)):
            if i % 2 == 0:
                aliceScore += stones[i]
            else:
                bobScore += stones[i]
        if aliceScore > bobScore:
            return 1
        elif aliceScore < bobScore:
            return -1
        else:
            return 0