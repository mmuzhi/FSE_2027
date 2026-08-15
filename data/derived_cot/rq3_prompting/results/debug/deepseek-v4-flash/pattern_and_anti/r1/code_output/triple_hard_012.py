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

        n = len(word)

        def forbidden_prefix_len(i: int, j: int) -> int:
            t = trie
            limit = min(j, i + max_len)
            for pos in range(i, limit):
                c = word[pos]
                if c not in t:
                    return 0
                t = t[c]
                if "end" in t:
                    return pos - i + 1
            return 0

        ans = 0
        j = n

        for i in range(n - 1, -1, -1):
            blocked = forbidden_prefix_len(i, j)
            if blocked:
                j = i + blocked - 1
            ans = max(ans, j - i)

        return ans