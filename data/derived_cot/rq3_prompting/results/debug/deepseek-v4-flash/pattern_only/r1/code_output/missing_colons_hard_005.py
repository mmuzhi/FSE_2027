from typing import List

class Solution:
    def longestValidSubstring(self, word: str, forbidden: List[str]) -> int:
        trie = {}
        max_len = 0

        for f in forbidden:
            max_len = max(max_len, len(f))
            t = trie
            for c in f:
                if c not in t:
                    t[c] = {}
                t = t[c]
            t["end"] = True

        def isForbidden(i: int, j: int):
            t = trie
            limit = min(j, i + max_len)
            for k in range(i, limit):
                c = word[k]
                if c not in t:
                    return False
                t = t[c]
                if "end" in t:
                    return k - i + 1
            return False

        res = 0
        j = len(word)

        for i in range(len(word) - 1, -1, -1):
            truc = isForbidden(i, j)
            if truc:
                j = i + truc - 1
            res = max(res, j - i)

        return res