import math

mod = 10**9 + 7

class Solution:
    def countAnagrams(self, s: str) -> int:
        l = s.split()
        ans = 1
        for i in l:
            d = {}
            for j in i:
                d[j] = d.get(j, 0) + 1  # count frequencies correctly
            
            duplicates = 1
            for freq in d.values():
                duplicates *= math.factorial(freq)
            
            n = len(i)
            curr = math.factorial(n) // duplicates
            ans = (ans * curr) % mod
        
        return ans