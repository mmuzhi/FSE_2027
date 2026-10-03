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

        def isForbidden(s: str) -> int:
            t = trie
            length = 0
            for c in s:
                if c not in t:
                    return 0
                t = t[c]
                length += 1
                if "end" in t:
                    return length
            return 0

        n = len(word)
        j = n
        res = 0
        for i in range(n - 1, -1, -1):
            truc = isForbidden(word[i:j])
            if truc:
                j = i + truc - 1
            res = max(res, j - i)
        return res