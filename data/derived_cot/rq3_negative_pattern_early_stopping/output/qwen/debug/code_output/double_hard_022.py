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
                    return False, 0
                t = t[c]
                if "end" in t:
                    return True, idx + 1
            return False, 0
        
        res = 0
        j = len(word)
        for i in range(len(word) - 1, -1, -1):
            # Check substring word[i:j] for forbidden substring
            found, length = isForbidden(word[i:j])
            if found:
                j = i + length - 1
            res = max(res, j - i)
        return res
