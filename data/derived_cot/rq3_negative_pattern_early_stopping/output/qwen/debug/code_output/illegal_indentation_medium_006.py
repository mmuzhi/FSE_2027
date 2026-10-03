from typing import List
from collections import Counter

class Solution:
    def wordSubsets(self, words1: List[str], words2: List[str]) -> List[str]:
        w2 = Counter()
        for word in words2:
            cnt = Counter(word)
            for char, count in cnt.items():
                if count > w2[char]:
                    w2[char] = count
        return [w1 for w1 in words1 if Counter(w1) >= w2]