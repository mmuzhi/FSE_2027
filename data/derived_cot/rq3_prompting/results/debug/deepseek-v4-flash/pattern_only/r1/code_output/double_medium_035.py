from typing import List

class Solution:
    def maximumNumber(self, num: str, change: List[int]) -> str:
        num = list(num)
        on = False
        for i, ch in enumerate(num):
            x = int(ch)
            if change[x] > x:
                on = True
                num[i] = str(change[x])
            elif on and change[x] < x:
                break
        return "".join(num)