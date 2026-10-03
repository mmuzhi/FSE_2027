from typing import List

class Solution:
    def longestValidSubstring(self, word: str, forbidden: List[str]) -> int:
        trie = {}
        for f in forbidden:
            t = trie
            for c in reversed(f):
                if c not in t:
                    t[c] = {}
                t = t[c]
            t["end"] = True

        left = 0
        res = 0
        for right in range(len(word)):
            node = trie
            for p in range(right, left - 1, -1):
                c = word[p]
                if c not in node:
                    break
                node = node[c]
                if "end" in node:
                    left = max(left, p + 1)
                    break
            res = max(res, right - left + 1)

        return res