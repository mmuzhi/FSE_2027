class Solution:
    def getLargestOutlier(self, nums: List[int]) -> int:
        total = sum(nums)
        from collections import Counter
        freq = Counter(nums)
        max_outlier = -10**9  # a very small number
        
        for x in nums:
            # Calculate y from the equation: total - x = 2*y
            if (total - x) % 2 != 0:
                continue
            y = (total - x) // 2
            # Check if y is in the array with sufficient multiplicity
            if x == y:
                if freq[y] >= 2:
                    max_outlier = max(max_outlier, x)
            else:
                if freq[y] >= 1:
                    max_outlier = max(max_outlier, x)
        
        return max_outlier