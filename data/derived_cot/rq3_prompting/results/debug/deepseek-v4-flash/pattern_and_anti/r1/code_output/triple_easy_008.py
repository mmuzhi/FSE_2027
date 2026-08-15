from typing import List

class Solution:
    def selfDividingNumbers(self, left: int, right: int) -> List[int]:
        res = []
        for i in range(left, right + 1):
            ch = True
            for j in str(i):
                d = int(j)
                if d == 0 or i % d != 0:
                    ch = False
                    break
            if ch:
                res.append(i)
        return res