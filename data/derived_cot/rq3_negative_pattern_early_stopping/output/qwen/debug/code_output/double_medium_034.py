class Solution:
    def lexicalOrder(self, n: int) -> List[int]:
        lst = [str(i) for i in range(1, n+1)]
        lst.sort()
        return [int(x) for x in lst]