from typing import List

class Solution:
    def longestValidSubstring(self, word: str, forbidden: List[str]) -> int:
        trie = {}
        max_len = 0
        for f in forbidden:
            t = trie
            for c in f:
                if c not in t:
                    t[c] = {}
                t = t[c]
            t["end"] = True
            max_len = max(max_len, len(f))

        def isForbidden(s):
            t = trie
            counter = 0
            for c in s:
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
            truc = isForbidden(word[i:min(j, i + max_len)])
            if truc:
                j = i + truc - 1
            res = max(res, j - i)
        return res