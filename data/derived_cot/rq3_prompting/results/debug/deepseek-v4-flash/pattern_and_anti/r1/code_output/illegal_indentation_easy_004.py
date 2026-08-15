from typing import List
from collections import Counter

class Solution:
    def countCharacters(self, words: List[str], chars: str) -> int:
        ans = []
        d1 = Counter(chars)

        for word in words:
            d2 = Counter(word)
            if all(ch in d1 and d2[ch] <= d1[ch] for ch in d2):
                ans.append(len(word))

        return sum(ans)