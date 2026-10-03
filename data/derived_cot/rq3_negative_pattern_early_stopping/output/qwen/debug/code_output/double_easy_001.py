class Solution:
    def canThreePartsEqualSum(self, arr: List[int]) -> bool:
        total = sum(arr)
        if total % 3 != 0:
            return False
        each_sum = total // 3
        count = 0
        current = 0
        for i in range(len(arr)):
            current += arr[i]
            if current == each_sum:
                count += 1
                current = 0
            if count == 2 and i < len(arr)-1:
                return True
        return False