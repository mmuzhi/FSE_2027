from typing import List

class Solution:
    def canThreePartsEqualSum(self, arr: List[int]) -> bool:
        total = sum(arr)
        if total % 3 != 0:
            return False

        target = total // 3
        current = 0
        parts = 0
        n = len(arr)

        for i, x in enumerate(arr):
            current += x
            if current == target:
                current = 0
                parts += 1

            if parts == 2:
                return i < n - 1

        return False