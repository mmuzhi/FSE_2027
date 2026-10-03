from typing import List

class Solution:
    def longestValidSubstring(self, word: str, forbidden: List[str]) -> int:
        trie = {}
        for f in forbidden:
            node = trie
            for ch in f:
                if ch not in node:
                    node[ch] = {}
                node = node[ch]
            node['#'] = True  # mark end of a word

        max_len = 0
        n = len(word)
        right = n  # current right boundary (exclusive)

        for left in range(n - 1, -1, -1):
            node = trie
            for offset in range(left, min(left + 10, right)):
                ch = word[offset]
                if ch not in node:
                    break
                node = node[ch]
                if '#' in node:
                    right = offset + 1  # adjust right so that this word is excluded
                    break
            max_len = max(max_len, right - left)

        return max_len