class Solution:
    def longestValidSubstring(self, word: str, forbidden: List[str]) -> int:
        # Build a trie from forbidden words
        trie = {}
        for f in forbidden:
            t = trie
            for c in f:
                if c not in t:
                    t[c] = {}
                t = t[c]
            t["end"] = True
        
        def isForbidden(s):
            # Use the trie to check if s contains any forbidden substring.
            # We'll search for any occurrence of a forbidden word in s.
            t = trie
            n = len(s)
            for i in range(n):
                # Reset the trie state for each starting position
                temp = trie
                for j in range(i, n):
                    c = s[j]
                    if c not in temp:
                        break
                    temp = temp[c]
                    if "end" in temp:
                        return True
            return False
        
        res = 0
        j = 0
        n = len(word)
        for i in range(n):
            # We'll move j to the right until the substring [i:j] contains a forbidden substring.
            # But we need to check [i:j] for any forbidden substring.
            # We start from j = i.
            while j < n and not isForbidden(word[i:j]):
                j += 1
            res = max(res, j - i)
        return res