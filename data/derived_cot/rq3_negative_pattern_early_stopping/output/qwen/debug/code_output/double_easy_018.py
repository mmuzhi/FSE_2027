from collections import Counter

class Solution:
    def countCharacters(self, words: List[str], chars: str) -> int:
        d1 = Counter(chars)
        total = 0
        for word in words:
            d2 = Counter(word)
            if all(d2[k] <= d1.get(k, 0) for k in d2):
                total += len(word)
        return total