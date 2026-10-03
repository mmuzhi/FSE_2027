from typing import List

class Solution:
    def maximumNumber(self, num: str, change: List[int]) -> str:
        num = list(num)
        on = False
        for i, ch in enumerate(num):
            x = int(ch)
            if not on:
                if change[x] > x:
                    on = True
                    num[i] = str(change[x])
            else:
                if change[x] >= x:
                    num[i] = str(change[x])
                else:
                    break
        return "".join(num)