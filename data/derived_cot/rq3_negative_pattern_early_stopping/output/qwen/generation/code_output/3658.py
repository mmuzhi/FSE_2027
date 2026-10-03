class Solution:
    def minDifference(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 1:
            return 0
        
        # Separate the fixed numbers and the positions of -1
        fixed = [num for num in nums if num != -1]
        missing = [i for i, num in enumerate(nums) if num == -1]
        
        # If there are no fixed numbers, then we can choose any two numbers, but the array length is at least 2, so we can set all to same number.
        if not fixed:
            return 0
        
        # If there are no missing numbers, then we just compute the max adjacent difference.
        if not missing:
            min_val = float('inf')
            max_val = float('-inf')
            for i in range(n-1):
                a, b = nums[i], nums[i+1]
                if abs(a - b) > max_val:
                    max_val = abs(a - b)
            return max_val
        
        # We need to consider the entire array, including fixed numbers and the positions of missing numbers.
        # The idea is that the missing numbers will be replaced by two numbers, x and y, and we want to minimize the maximum adjacent difference.
        # The key observation is that the maximum adjacent difference will be determined by the gaps between fixed numbers and the gaps introduced by the missing numbers.

        # Let's collect the fixed numbers and the positions of missing numbers. But actually, we can think of the array as a sequence of fixed numbers with gaps (missing numbers) in between.

        # We can consider the entire array and the transitions between fixed numbers. The missing numbers can be thought of as being replaced by numbers that are either x or y, so they can bridge the gaps between fixed numbers.

        # The problem can be transformed: we have a sequence of fixed numbers (ignoring the missing ones) and we need to assign x and y to the missing spots such that the maximum adjacent difference is minimized.

        # Another approach: the answer is the minimum possible maximum adjacent difference. We can use binary search on the maximum allowed adjacent difference (let's call it D) and check if it's possible to choose x and y such that after replacement, all adjacent differences are <= D.

        # But how to check for a given D? We need to see if there exist two numbers x and y such that for every adjacent pair (a, b) in the array (after replacement), |a - b| <= D.

        # However, note that the replacements are only for -1, and the fixed numbers are fixed. So the adjacent pairs that involve fixed numbers must be satisfied by the chosen x and y.

        # Alternatively, we can consider that the entire array must be "covered" by two numbers. The maximum adjacent difference will be determined by the gaps between fixed numbers and the gaps between the chosen x and y and the fixed numbers.

        # Let me think of the fixed numbers as anchors. The missing numbers can be thought of as being in between these anchors. The adjacent differences that matter are between consecutive fixed numbers (with missing numbers in between) and between fixed numbers and the chosen x/y.

        # Actually, the problem is similar to "minimum added value to fill gaps" but with two numbers.

        # Steps:

        # 1. Extract the fixed numbers and their positions. But actually, we can consider the entire array and the transitions.

        # 2. The maximum adjacent difference after replacement must be at least the maximum difference between consecutive fixed numbers (if we ignore the missing ones). Because even if we fill the missing numbers optimally, the gap between two fixed numbers that are far apart must be bridged by the chosen x and y.

        # 3. But note: the missing numbers can be filled with two numbers, so the gap between two fixed numbers can be bridged by a sequence of x and y. The worst-case adjacent difference in that gap would be the maximum of |fixed[i] - x|, |x - y|, |y - fixed[j]|, etc.

        # Actually, the problem is more complex. Let me consider the example: [1,2,-1,10,8]. The fixed numbers are 1,2,10,8. The gaps are between 2 and 10 (with one missing) and between 10 and 8 (with no missing). The answer is 4.

        # How did they get 4? They chose 6 and 7. Then the array becomes [1,2,6,10,8]. The adjacent differences are 1,4,4,2. The maximum is 4.

        # Another example: [-1,-1,-1] -> output 0. They choose (4,4) so all are 4, so adjacent differences are 0.

        # Example 3: [-1