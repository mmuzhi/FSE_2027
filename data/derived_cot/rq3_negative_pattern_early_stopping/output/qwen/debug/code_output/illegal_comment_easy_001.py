class Solution:
    def canThreePartsEqualSum(self, arr: List[int]) -> bool:
        total = sum(arr)
        if total % 3 != 0:
            return False
        each_sum = total // 3
        count = 0
        current_sum = 0
        for i in range(len(arr)):
            current_sum += arr[i]
            if current_sum == each_sum and count == 0:
                count += 1
            elif current_sum == 2 * each_sum and count == 1:
                count += 1
        return count == 2
