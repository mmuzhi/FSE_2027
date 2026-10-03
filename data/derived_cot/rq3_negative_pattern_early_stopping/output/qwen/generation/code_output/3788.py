class Solution:
    def maxSum(self, nums: List[int]) -> int:
        n = len(nums)
        best = -10**9
        # We'll use a two-pointer (sliding window) that considers the original array and allows non-contiguous selection?
        # But note: The contiguous block in the kept set is defined by the kept set's order.
        # However, we can use a different approach: 
        # We are allowed to drop any elements, so we can choose any subsequence. Then from that subsequence, we choose a contiguous block (consecutive in the subsequence) that has distinct elements.
        # But the optimal solution will be to choose a contiguous block (in the kept set) that is distinct and has maximum sum.
        # We can use a two-pointer (sliding window) that maintains a window of distinct elements, but the window is not required to be contiguous in the original array.
        # But then, how to iterate? 
        # Actually, we can use a two-pointer (sliding window) that considers the original array and allows non-contiguous selection? 
        # But then, the window is not contiguous. 
        # Alternatively, we can consider: 
        # We want to find a set of indices (in increasing order) such that the elements are distinct and the sum is maximized.
        # But then, the contiguous block we choose is the entire set.
        # But that is not necessarily true: The problem allows us to choose a contiguous block from the kept set. But if the entire kept set is distinct, then the entire kept set is a valid contiguous block.
        # But if the entire kept set is not distinct, then we might choose a subset (a consecutive part) that is distinct and has a higher sum.
        # However, the optimal solution might be to choose a contiguous block that is not the entire kept set.
        # But note: We are allowed to drop arbitrarily, so we can choose to keep only the contiguous block we want.
        # Therefore, the problem reduces to: 
        # Find a contiguous block (in the original array) that has distinct elements and has maximum sum? 
        # But wait, the contiguous block does not have to be contiguous in the original array. 
        # Actually, no: The contiguous block we choose is contiguous in the kept set. The kept set is the original array's order. 
        # But if we choose a set of indices that are not contiguous in the original array, then the contiguous block we choose is the entire set (if we keep only these indices) and the set must be distinct.
        # So the problem is: 
        # Find a set of indices (in increasing order) such that the elements are distinct and the sum is maximized.
        # But then, the contiguous block is the entire set.
        # But note: The problem does not require the contiguous block to be contiguous in the original array. 
        # So we can choose any set of indices (distinct elements) and the sum is the sum of those elements.
        # But then, the answer is simply the maximum sum of a set of distinct elements (not necessarily contiguous in the original array) from the array.
        # But wait, consider: 
        # Example 2: [1,1,0,1,1] -> the maximum sum is 1 (from [1]). 
        # But if we choose the set {1} (distinct) then the sum is 1.
        # Example 3: [1,2,-1,-2,1,0,-1] -> the maximum sum is 3 (from [2,1]).
        # But if we choose the set {2,1} (distinct) then the sum is 3.
        # But note: The set {2,1} is not contiguous in the original array? Actually, in the original array, the elements 2 and 1 are at indices 1 and 4. But the kept set is {1,2} (the elements) and the contiguous block is the entire kept set (which is [2,1] in the kept set's order). 
        # But the kept set's order is the original array's order. So the kept set for {2,1} is [2,1] (because in the original array, 2 comes before 1). 
        # But then, the contiguous block is [2,1] (distinct) and the sum is 3.
        # But what if we choose a set that is not contiguous in the original array? 
        # For example, in [1,2,3,1,2,4], the set {1,2,3,4} has sum 10. 
        # But note: The kept set is the set of indices we keep. The order is the original array's order. 
        # So the problem is: