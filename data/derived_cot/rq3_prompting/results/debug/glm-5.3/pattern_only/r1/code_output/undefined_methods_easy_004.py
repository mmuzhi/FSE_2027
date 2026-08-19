class Solution:
    def minimumOperations(self, nums: List[int]) -> int:
        uniq_non_zero = set()
        for num in nums:
            if num == 0:
                continue
            uniq_non_zero.add(num)
        return self.uniqueCount(uniq_non_zero)

    def uniqueCount(self, num_set: set) -> int:
        return len(num_set)