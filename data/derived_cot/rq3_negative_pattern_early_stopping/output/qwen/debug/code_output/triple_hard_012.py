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
            for i in range(len(s)):
                temp = trie
                for j in range(i, len(s)):
                    c = s[j]
                    if c not in temp:
                        break
                    temp = temp[c]
                    if "end" in temp:
                        return True
            return False
        
        n = len(word)
        j = n
        for i in range(n-1, -1, -1):
            # Check substring word[i:j]
            if isForbidden(word[i:j]):
                # We need to find the smallest j such that word[i:j] is valid
                # But we don't know the exact j, so we move j to i (meaning the substring is empty) and then break?
                # Actually, we want to find the longest valid substring ending at i+j-1, so we need to move j until the substring is valid.
                # But we don't know how much to move, so we can do a while loop to find the smallest j that makes the substring valid.
                # However, we are iterating i from the end, so we can set j = i (meaning the substring is empty) and then continue.
                j = i
            else:
                # The substring word[i:j] is valid, so update the result
                res = max(res, j - i)
        return res if 'res' in locals() else 0

    def __init__(self):
        self.res = 0

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
            for i in range(len(s)):
                temp = trie
                for j in range(i, len(s)):
                    c = s[j]
                    if c not in temp:
                        break
                    temp = temp[c]
                    if "end" in temp:
                        return True
            return False
        
        n = len(word)
        j = n
        res = 0
        for i in range(n-1, -1, -1):
            if isForbidden(word[i:j]):
                j = i
            else:
                res = max(res, j - i)
        return res
