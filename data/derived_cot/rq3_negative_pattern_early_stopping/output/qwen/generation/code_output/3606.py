class Solution:
    def minElement(self, nums: List[int]) -> int:
        transformed = []
        for num in nums:
            total = 0
            for digit in str(num):
                total += int(digit)
            transformed.append(total)
        return min(transformed)