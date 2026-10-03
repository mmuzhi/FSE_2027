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
            cnt = 0
            for c in s:
                if c not in t:
                    return False
                t = t[c]
                cnt += 1
                if "end" in t:
                    return cnt
            return False
        
        res = 0
        j = len(word)  # exclusive right boundary
        for i in range(len(word) - 1, -1, -1):
            truc = isForbidden(word[i:j])
            if truc:
                j = i + truc - 1
            res = max(res, j - i)
        return res