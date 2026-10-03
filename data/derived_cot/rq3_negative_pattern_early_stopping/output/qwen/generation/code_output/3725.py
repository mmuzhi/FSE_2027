class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        n = len(nums)
        # We'll compute the sum of min and sum of max separately for subarrays of length 1 to k.
        # For the sum of min:
        #   We use a deque to maintain the increasing order (for min) and decreasing order (for max).
        #   We'll use two passes: one for min and one for max.
        #   But note: the standard method for "sum of min of all subarrays" without length constraint uses the next greater element to determine the range where the current element is the minimum.
        #   However, we have a constraint: the subarray must be of length at most k.

        # We can modify the standard method by limiting the window to k.

        # For the min part:
        #   We want to compute for each element, the contribution of being the minimum in a subarray that ends at or before the element and has length at most k.
        #   We can use a deque to maintain the next greater element, but we also need to consider the left boundary (at least one element) and the right boundary (the element itself and the next greater element, but also limited by k).

        # Alternatively, we can use a two-pointer and update the min and max for each window of size from 1 to k, but that is O(n*k) which is too slow.

        # We need an efficient method.

        # Let's use the standard method for "sum of min of all subarrays" but with a constraint of at most k.

        # Steps for min:
        #   We traverse from left to right, and for each element, we want to find the previous element that is less than or equal to it (to maintain increasing order) and the next element that is less than it (or the boundary) to determine the range where the current element is the minimum, but then we must also ensure that the subarray does not exceed k in length.

        # Actually, we can use a deque to maintain the indices of elements in increasing order (for min). Then, for each element at index i, the left boundary for the subarray where nums[i] is the minimum is the previous element that is less than nums[i] (or the start of the array) and the right boundary is the next element that is less than nums[i] (or the end of the array) but also we cannot have a subarray longer than k.

        # However, the standard method for "sum of min of all subarrays" without length constraint uses:
        #   Let left1[i] be the index of the previous element that is less than nums[i] (or -1 if none)
        #   Let right1[i] be the index of the next element that is less than or equal to nums[i] (or n if none)
        #   Then the number of subarrays where nums[i] is the minimum is (i - left1[i]) * (right1[i] - i)
        #   Then the contribution is nums[i] * (i - left1[i]) * (right1[i] - i)

        # But with the constraint of at most k, we must also ensure that the subarray does not exceed k in length. 

        # We can modify: 
        #   The subarray must end at or before i and start at or after left1[i]+1, and the length must be <= k. So the right boundary is min(right1[i], i+k) and the left boundary is max(left1[i]+1, i-k+1) [because the subarray starting at j and ending at i must have length <= k, so j >= i-k+1]. 

        # But note: the standard method without length constraint uses the next smaller element to the left and right to define the range. With the length constraint, we have to limit the subarray to at most k elements.

        # Actually, we can use a two-pointer to compute the left and right boundaries for each element for the min and max, but then we have to consider the length constraint.

        # Alternatively, we can use a deque to maintain the min and max for the current window (of length up to k) and then update the sum as we move the window.

        # But note: the total number of subarrays is n*k, which is too many to iterate.

        # We need to use the standard method with the length constraint.

        # Let's define for the min part:
        #   We want to compute for each element i, the number of subarrays where nums[i] is the minimum and the subarray has length at most k.

        #   The subarray must include i and have length at most k. The left boundary for the subarray is from max(0, i-k+1) to the