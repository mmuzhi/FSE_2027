from collections import Counter

class Solution:
    def maxDifference(self, s: str) -> int:
        count = Counter(s)
        even_freqs = [freq for freq in count.values() if freq % 2 == 0]
        odd_freqs = [freq for freq in count.values() if freq % 2 != 0]
        return max(odd_freqs) - min(even_freqs)