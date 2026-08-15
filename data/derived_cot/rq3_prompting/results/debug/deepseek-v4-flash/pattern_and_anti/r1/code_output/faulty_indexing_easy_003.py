from typing import List
from collections import Counter
import math

class Solution:
    def hasGroupsSizeX(self, deck: List[int]) -> bool:
        counts = Counter(deck)
        g = 0
        for c in counts.values():
            g = math.gcd(g, c)
        return g >= 2