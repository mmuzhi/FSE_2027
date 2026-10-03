class Solution:
    def maxGoodNumber(self, nums: List[int]) -> int:
        from itertools import permutations
        max_val = 0
        for perm in permutations(nums):
            binary_str = ''.join(bin(num)[2:] for num in perm)
            current_val = int(binary_str, 2)
            if current_val > max_val:
                max_val = current_val
        return max_val