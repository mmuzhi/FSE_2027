import math

mod = 10**9 + 7

class Solution:
    def countAnagrams(self, s: str) -> int:
        ans = 1

        for word in s.split():
            freq = {}

            for ch in word:
                if freq.get(ch):
                    freq[ch] += 1
                else:
                    freq[ch] = 1

            duplicates = 1
            for cnt in freq.values():
                duplicates *= math.factorial(cnt)

            curr = math.factorial(len(word)) // duplicates
            ans = (ans * curr) % mod

        return ans