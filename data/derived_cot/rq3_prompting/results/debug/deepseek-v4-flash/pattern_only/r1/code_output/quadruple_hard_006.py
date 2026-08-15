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

        def isForbidden(l: int, r: int):
            t = trie
            cnt = 0
            for k in range(l, r):
                c = word[k]
                if c not in t:
                    return False
                t = t[c]
                cnt += 1
                if "end" in t:
                    return cnt
            return False

        ans = 0
        j = len(word)

        for i in range(len(word) - 1, -1, -1):
            cnt = isForbidden(i, j)
            if cnt:
                j = i + cnt - 1
            ans = max(ans, j - i)

        return ans