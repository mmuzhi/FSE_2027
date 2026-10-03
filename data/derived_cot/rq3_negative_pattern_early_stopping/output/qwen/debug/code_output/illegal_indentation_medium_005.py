class Solution:
    def maximumNumber(self, num: str, change: List[int]) -> str:
        num_list = list(num)
        for i in range(len(num_list)):
            x = int(num_list[i])
            if x < change[x]:
                num_list[i] = str(change[x])
        return "".join(num_list)
