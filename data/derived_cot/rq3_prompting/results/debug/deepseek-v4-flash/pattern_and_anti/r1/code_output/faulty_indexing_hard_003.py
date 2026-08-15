from typing import List

class Solution:
    def longestValidSubstring(self, word: str, forbidden: List[str]) -> int:
        trie = {}
        for f in forbidden:
            t = trie
            for c in f:
                if c not in t:
                    t[c] = {}
                t = t[c]
            t["end"] = True

        def isForbidden(start, end):
            t = trie
            counter = 0
            for idx in range(start, end):
                c = word[idx]
                if c not in t:
                    return False
                t = t[c]
                counter += 1
                if "end" in t:
                    return counter
            return False

        res = 0
        j = len(word)
        for i in range(len(word) - 1, -1, -1):
            truc = isForbidden(i, j)
            if truc:
                j = min(j, i + truc - 1)
            res = max(res, j - i)
        return res