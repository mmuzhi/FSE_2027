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

        def forbidden_prefix_length(start: int, end: int) -> int:
            if max_len == 0:
                return 0
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

        ans = 0
        right = len(word)
        for left in range(len(word) - 1, -1, -1):
            length = forbidden_prefix_length(left, right)
            if length:
                right = left + length - 1
            ans = max(ans, right - left)
        return ans