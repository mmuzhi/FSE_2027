from typing import List

class Solution:
    def selfDividingNumbers(self, left: int, right: int) -> List[int]:
        res = []
        for i in range(left, right + 1):
            ch = True
            for j in str(i):
                if int(j) == 0 or i % int(j) != 0:
                    ch = False
                    break
            if ch:
                res.append(i)
        return res