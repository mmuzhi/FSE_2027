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

        if max_len == 0:
            return len(word)

        n = len(word)
        ans = 0
        right = n

        def forbidden_prefix_len(start: int, end: int) -> int:
            t = trie
            limit = min(end, start + max_len)
            for pos in range(start, limit):
                c = word[pos]
                if c not in t:
                    return 0
                t = t[c]
                if "end" in t:
                    return pos - start + 1
            return 0

        for left in range(n - 1, -1, -1):
            length = forbidden_prefix_len(left, right)
            if length:
                right = left + length - 1
            ans = max(ans, right - left)

        return ans