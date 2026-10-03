import itertools

class Solution:
    def totalNumbers(self, digits: List[int]) -> int:
        perms = itertools.permutations(digits, 3)
        seen = set()
        for p in perms:
            if p[0] == 0:
                continue
            if p[2] % 2 != 0:
                continue
            num = p[0]*100 + p[1]*10 + p[2]
            seen.add(num)
        return len(seen)