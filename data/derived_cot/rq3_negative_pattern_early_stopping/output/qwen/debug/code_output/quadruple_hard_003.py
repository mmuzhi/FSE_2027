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
            for idx, c in enumerate(s):
                if c not in t:
                    return 0
                t = t[c]
                if "end" in t:
                    return idx + 1
            return 0
        
        n = len(word)
        res = 0
        j = n + 1
        for i in range(n-1, -1, -1):
            if j > i:
                truc = isForbidden(word[i:j])
                if truc:
                    j = i + truc - 1
            res = max(res, j - i)
        return res