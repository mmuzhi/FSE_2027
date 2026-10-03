class Solution:
    def maximumNumber(self, num: str, change: List[int]) -> str:
        num = list(num)
        on = False
        for i, ch in enumerate(num):
            x = int(ch)
            if x < change[x]:
                on = True
                num[i] = str(change[x])
            elif x > change[x] and on:
                break
        return "".join(num)