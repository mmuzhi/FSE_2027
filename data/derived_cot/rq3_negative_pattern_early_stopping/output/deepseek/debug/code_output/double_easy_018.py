from typing import List
from collections import Counter

class Solution:
    def countCharacters(self, words: List[str], chars: str) -> int:
        ans = []
        d1 = Counter(chars)
        for word in words:
            d2 = Counter(word)
            if all(d2[k] <= d1.get(k, 0) for k in d2):
                ans.append(len(word))
        return sum(ans)