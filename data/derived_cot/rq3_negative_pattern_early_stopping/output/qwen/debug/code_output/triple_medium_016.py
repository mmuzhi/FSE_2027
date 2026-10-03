class Solution:
    def maximumNumber(self, num: str, change: List[int]) -> str:
        num = list(num)
        for i, ch in enumerate(num): 
            x = int(ch)
            if x < change[x]: 
                num[i] = str(change[x])
        return "".join(num)