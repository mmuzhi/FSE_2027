from typing import List

class Solution:
    def longestValidSubstring(self, word: str, forbidden: List[str]) -> int:
        if any(f == "" for f in forbidden):
            return 0

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

        def first_forbidden(i: int, j: int) -> int:
            t = trie
            for k in range(i, min(j, i + max_len)):
                c = word[k]
                if c not in t:
                    return 0
                t = t[c]
                if "end" in t:
                    return k - i + 1
            return 0

        ans = 0
        j = len(word)

        for i in range(len(word) - 1, -1, -1):
            length = first_forbidden(i, j)
            if length:
                j = min(j, i + length - 1)
            ans = max(ans, j - i)

        return ans