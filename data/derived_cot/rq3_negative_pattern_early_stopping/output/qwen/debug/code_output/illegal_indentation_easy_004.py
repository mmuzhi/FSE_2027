class Solution:
    def countCharacters(self, words: List[str], chars: str) -> int:
        d1 = Counter(chars)
        ans = 0
        for word in words:
            d2 = Counter(word)
            valid = True
            for char, count in d2.items():
                if count > d1.get(char, 0):
                    valid = False
                    break
            if valid:
                ans += len(word)
        return ans
