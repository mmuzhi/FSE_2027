from typing import List
import collections
import math

class Solution:
    def hasGroupsSizeX(self, deck: List[int]) -> bool:
        count = collections.Counter(deck)
        g = 0
        for c in count.values():
            g = math.gcd(g, c)
        return g >= 2