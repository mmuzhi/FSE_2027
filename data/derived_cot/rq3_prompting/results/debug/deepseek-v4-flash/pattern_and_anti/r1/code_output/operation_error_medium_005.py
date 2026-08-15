from typing import List

class Solution:
    def findLongestWord(self, s: str, d: List[str]) -> str:
        res = ''
        for cand in d:
            if self.find(s, cand) and (len(cand) > len(res) or (len(cand) == len(res) and cand < res)):
                res = cand
        return res

    def find(self, s: str, target: str) -> bool:
        i, j = 0, 0
        while i < len(s) and j < len(target):
            if s[i] == target[j]:
                i += 1
                j += 1
            else:
                i += 1
        return j == len(target)