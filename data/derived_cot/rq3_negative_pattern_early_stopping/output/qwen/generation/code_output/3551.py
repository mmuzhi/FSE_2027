class Solution:
    def maximumSubarrayXor(self, nums: List[int], queries: List[List[int]]) -> List[int]:
        n = len(nums)
        # Precompute the maximum XOR score for every subarray? But n can be up to 2000, so O(n^2) subarrays, which is 4e6, which is acceptable in Python if done carefully.
        # But then, for each query, we need to answer the maximum XOR score in a range. We can precompute a 2D table dp[i][j] for the maximum XOR score in the subarray from i to j, but that would be O(n^2) space and time, and then for each query, we need to find the maximum in a 2D range, which is O(n^2) per query, and q can be up to 10^5, so that's too slow.

        # Alternatively, we can precompute the maximum XOR score for every subarray and store it in a 2D array, then use a 2D segment tree or sparse table for range maximum queries. But building a sparse table for 2D range maximum query on a 2000x2000 array (4e6 elements) is acceptable in terms of memory (about 4e6 * 4 bytes = 16 MB) but the time to build is O(n^2 log n) which is acceptable for n=2000? Actually, 2000^2 is 4e6, and log2(2000) is about 11, so 44e6 operations, which is acceptable in C++ but in Python might be borderline. But then, we have 10^5 queries, each query is a rectangle in the 2D table? Actually, the query is for a contiguous subarray in the original array, but the maximum XOR score is defined for every contiguous subarray. So we need to answer: for a given range [l, r], what is the maximum value of dp[i][j] for all i, j such that l <= i <= j <= r.

        # But note: the maximum XOR score for a subarray is defined by the process. We need to compute the score for every contiguous subarray.

        # How to compute the score for a subarray? 

        # Let f(a) be the XOR score of array a. The process is:
        #   While len(a) > 1:
        #       a = [a[0]^a[1], a[1]^a[2], ..., a[n-2]^a[n-1]]   (this is the replacement)
        #       then remove the last element (so the new array is a[0..n-2] after the replacement)
        #   Then the score is the last remaining element.

        # But note: the operation is done simultaneously on all elements except the last, and then the last element is removed. 

        # Let me compute for [2,8,4]:
        #   Step 1: [2^8, 8^4] = [10, 12] -> then remove last element: [10]. So score is 10.

        # But the example says the score for [2,8,4] is 6. 

        # Wait, there's a discrepancy. 

        # Let me re-read the example: 
        #   "In the first query, nums[0..2] has 6 subarrays [2], [8], [4], [2,8], [8,4], and [2,8,4] each with a respective XOR score of 2, 8, 4, 10, 12, and 6."

        # So the score for [2,8,4] is 6, not 10.

        # What's going on? 

        # Let me compute the score for [2,8,4] manually as per the example's expected answer:

        # Example says: [2,8,4] has score 6.

        # How? 

        # Maybe the operation is defined differently. 

        # Another possibility: the operation is: 
        #   In each step, you can choose to stop or do: 
        #       Replace each element a[i] with a[i] XOR a[i+1] for i from 0 to n-2, and then remove the last element.
        #   But then, the score is the element you end up with.

        # But then, for [2,8,4]:
        #   Step 1: [10,12] -> remove last -> [10]. Then stop. Score 10.

        # Alternatively, maybe the operation is: 
        #