from collections import Counter

class Solution:
    def wordSubsets(self, words1: List[str], words2: List[str]) -> List[str]:
        w2_max = Counter()
        for word in words2:
            c = Counter(word)
            for letter, count in c.items():
                if count > w2_max.get(letter, 0):
                    w2_max[letter] = count
        return [w1 for w1 in words1 if Counter(w1) >= w2_max]