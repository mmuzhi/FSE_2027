from typing import List

class Solution:
    def maximumNumber(self, num: str, change: List[int]) -> str:
        digits = list(num)
        started = False

        for i, ch in enumerate(digits):
            d = int(ch)
            if change[d] > d:
                started = True
                digits[i] = str(change[d])
            elif started and change[d] < d:
                break

        return "".join(digits)