from typing import List

class Solution:
    def maximumNumber(self, num: str, change: List[int]) -> str:
        num = list(num)
        started = False

        for i, ch in enumerate(num):
            x = int(ch)

            if x < change[x]:
                started = True
                num[i] = str(change[x])
            elif x > change[x] and started:
                break

        return "".join(num)