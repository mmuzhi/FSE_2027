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

        def forbidden_len(i: int, j: int) -> int:
            node = trie
            limit = min(j, i + max_len)
            for pos in range(i, limit):
                c = word[pos]
                if c not in node:
                    return 0
                node = node[c]
                if "end" in node:
                    return pos - i + 1
            return 0

        res = 0
        j = len(word)

        for i in range(len(word) - 1, -1, -1):
            truc = forbidden_len(i, j)
            if truc:
                j = i + truc - 1
            res = max(res, j - i)

        return res