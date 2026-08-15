from typing import List

class Solution:
    def restoreIpAddresses(self, s: str) -> List[str]:
        res = []
        cur = []

        def backtrack(i: int) -> None:
            if i == len(s) and len(cur) == 4:
                res.append(".".join(cur))
                return
            if len(cur) >= 4 or i >= len(s):
                return

            if s[i] == '0':
                cur.append(s[i])
                backtrack(i + 1)
                cur.pop()
                return

            for j in range(1, 4):
                if i + j > len(s):
                    break
                part = s[i:i + j]
                if int(part) <= 255:
                    cur.append(part)
                    backtrack(i + j)
                    cur.pop()

        backtrack(0)
        return res