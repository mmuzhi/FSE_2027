from typing import List
from collections import Counter

class Solution:
    def countCharacters(self, words: List[str], chars: str) -> int:
        d1 = Counter(chars)
        ans = 0

        for w in words:
            d2 = Counter(w)
            if all(d2[c] <= d1[c] for c in d2):
                ans += len(w)

        return ans