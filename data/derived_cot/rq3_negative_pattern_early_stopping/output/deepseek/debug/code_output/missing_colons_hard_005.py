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
        
        res = 0
        n = len(word)
        left = 0
        for right in range(n):
            t = trie
            for k in range(right, left - 1, -1):
                c = word[k]
                if c not in t:
                    break
                t = t[c]
                if "end" in t:
                    left = k + 1
                    break
            res = max(res, right - left + 1)
        return res