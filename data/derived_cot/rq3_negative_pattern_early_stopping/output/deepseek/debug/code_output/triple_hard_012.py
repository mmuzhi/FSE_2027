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
            node['#'] = True  # mark end of a forbidden word

        n = len(word)
        res = 0
        for i in range(n):
            node = trie
            j = i
            while j < n and word[j] in node:
                node = node[word[j]]
                if '#' in node:
                    break
                j += 1
            res = max(res, j - i)
        return res