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
        
        def isForbidden(s):
            t = trie
            for i, c in enumerate(s):
                if c not in t:
                    return 0
                t = t[c]
                if "end" in t:
                    return i + 1
            return 0
        
        res = 0
        j = len(word)
        for i in range(len(word) - 1, -1, -1):
            l = isForbidden(word[i:j])
            if l:
                j = i + l - 1
            res = max(res, j - i)
        return res