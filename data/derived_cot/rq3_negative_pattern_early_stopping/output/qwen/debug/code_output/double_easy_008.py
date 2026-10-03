class Solution:
    def plusOne(self, digits: List[int]) -> List[int]:
        s = ''.join(map(str, digits))
        i = int(s) + 1
        if i < 10:
            return [i]
        else:
            return list(map(int, str(i)))