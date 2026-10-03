import math

mod = 10**9 + 7

class Solution:
    def countAnagrams(self, s: str) -> int:
        words = s.split()
        ans = 1
        
        for word in words:
            freq = {}
            for char in word:
                freq[char] = freq.get(char, 0) + 1
            
            denominator = 1
            for count in freq.values():
                denominator *= math.factorial(count)
            
            numerator = math.factorial(len(word))
            distinct_permutations = numerator // denominator
            ans = (ans * distinct_permutations) % mod
        
        return ans