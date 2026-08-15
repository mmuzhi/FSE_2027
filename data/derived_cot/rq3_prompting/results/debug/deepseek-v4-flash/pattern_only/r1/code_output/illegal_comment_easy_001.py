from typing import List

class Solution:
    def canThreePartsEqualSum(self, arr: List[int]) -> bool:
        total = sum(arr)
        if total % 3 != 0:
            return False

        target = total // 3
        cur = 0
        count = 0

        for x in arr:
            cur += x
            if cur == target:
                cur = 0
                count += 1

        return count >= 3