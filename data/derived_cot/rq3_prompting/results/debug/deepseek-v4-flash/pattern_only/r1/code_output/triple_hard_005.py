from typing import List

class Solution:
    def longestValidSubstring(self, word: str, forbidden: List[str]) -> int:
        trie = {}
        max_len = 0

        for f in forbidden:
            max_len = max(max_len, len(f))
            node = trie
            for ch in f:
                if ch not in node:
                    node[ch] = {}
                node = node[ch]
            node["end"] = True

        def forbidden_prefix_length(left: int, right: int) -> int:
            node = trie
            limit = min(right, left + max_len)

            for pos in range(left, limit):
                ch = word[pos]
                if ch not in node:
                    return 0
                node = node[ch]
                if "end" in node:
                    return pos - left + 1

            return 0

        ans = 0
        right = len(word)

        for left in range(len(word) - 1, -1, -1):
            length = forbidden_prefix_length(left, right)
            if length:
                right = left + length - 1
            ans = max(ans, right - left)

        return ans