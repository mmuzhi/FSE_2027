class Solution:
    def plusOne(self, digits: List[int]) -> List[int]:
        s = ''.join(map(str, digits))
        num = int(s) + 1
        li = list(map(int, str(num)))
        return li