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

        def forbidden_prefix_length(start: int, end: int) -> int:
            t = trie
            length = 0
            for idx in range(start, end):
                c = word[idx]
                if c not in t:
                    return 0
                t = t[c]
                length += 1
                if "end" in t:
                    return length
            return 0

        n = len(word)
        ans = 0
        j = n

        for i in range(n - 1, -1, -1):
            L = forbidden_prefix_length(i, j)
            if L:
                j = i + L - 1
            ans = max(ans, j - i)

        return ans