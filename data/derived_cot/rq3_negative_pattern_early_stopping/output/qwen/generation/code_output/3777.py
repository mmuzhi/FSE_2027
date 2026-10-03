class Solution:
    def maxProduct(self, nums: List[int], k: int, limit: int) -> int:
        n = len(nums)
        # The alternating sum can range from -1800 to 1800 (since 150*12=1800)
        offset = 1800
        # We'll use dp[s] = maximum product for alternating sum s, but we need to consider the entire array
        # We'll do DP over the array indices, and update a dictionary of (alternating_sum) -> max_product for the current index.
        # But we need to consider that the subsequence can start at any point, so we need to reset the state at each element? 
        # Actually, we can do: for each element, we can either start a new subsequence (then alternating sum = nums[i], product = nums[i]) or extend an existing subsequence.
        # But the existing subsequence's length (even or odd) determines the sign of the next element.

        # We'll use a DP dictionary that maps alternating_sum to the maximum product for the subsequences ending at the current index (or up to the current index). But we need to consider all subsequences, not necessarily ending at the current index.

        # Alternatively, we can use a DP that goes through each element and updates a state (alternating_sum) with the maximum product. We'll use a dictionary for the current state (after processing each element) and update it by either including the current element or not.

        # Let dp be a dictionary: key = alternating_sum (shifted by offset), value = maximum product (<= limit) for that alternating_sum.
        # Initialize dp with {0: 1}? But note: we cannot have an empty subsequence. But we can start with no elements, then when we take the first element, we set alternating_sum = nums[i] and product = nums[i]. But we cannot have alternating_sum 0 from an empty subsequence because the problem says non-empty.

        # Actually, we can start by having no elements, then when we take the first element, we set alternating_sum = nums[i] and product = nums[i]. Then for the next element, we subtract, etc.

        # We'll do:
        # dp = {0: 1}  # base state: no elements, alternating_sum 0, product 1 (but then we cannot use this because we need non-empty). So we'll start with an empty set and then for each element, we update.

        # Instead, we can do:
        # Let dp be a dictionary that maps alternating_sum to the maximum product for the subsequences we've formed so far (from the elements processed so far). We start with an empty dictionary, and then for each element, we update.

        # But we need to consider that the subsequence must be in order, so we process from left to right.

        # We'll use a DP dictionary that is updated for each element. We'll start with an empty dictionary (or with the first element). Actually, we can initialize dp as empty, and then for each element, we create a new state dictionary.

        # Steps:
        # 1. Initialize dp as an empty dictionary.
        # 2. For each num in nums:
        #    a. Create a new_dp dictionary (or update dp in reverse order to avoid using the same element twice).
        #    b. For each (s, prod) in dp (from previous elements), we can either skip the current element, or take it.
        #    c. If we take it, then the new alternating_sum = s + (num if the current subsequence length is even? Actually, we don't track the length, but we can track the sign by the length. Alternatively, we can store the length along with the alternating_sum, but that would double the state space.

        # Alternatively, we can store the length of the subsequence along with the alternating_sum. But then the state space becomes (length, alternating_sum) which is 150*3601, which is acceptable.

        # But we can also note: the alternating_sum is the sum of the elements at even indices minus the sum of the elements at odd indices. The even indices are the ones that are positive, odd negative. The length of the subsequence is the number of elements. The next element (if added) will be at an index equal to the current length, so if the current length is even (0-indexed, meaning the next index is odd) then we subtract, else we add.

        # Actually, we can store the length of the subsequence (mod 2) and the alternating_sum. But then the state is (length % 2, alternating_sum). But the alternating_sum is the same as: (sum of elements at even indices) - (sum of elements at