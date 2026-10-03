class Solution:
    def findLongestWord(self, s: str, d: List[str]) -> str:
        res = ''
        for cand in d:
            if self.find(s, cand) and (len(cand) > len(res) or (len(cand) == len(res) and cand < res)):
                res = cand
        return res

    def find(self, s, word):
        i, j = 0, 0
        n, m = len(s), len(word)
        while i < n and j < m:
            if s[i] == word[j]:
                j += 1
            i += 1
        return j == m