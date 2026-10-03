class Solution:
    def numberOfSubsequences(self, nums: List[int]) -> int:
        n = len(nums)
        from collections import defaultdict
        # We'll use a dictionary to store the product of pairs and the indices (or just count) but we need to ensure the gap condition.
        # Alternatively, we can iterate and for each pair (i, j) (with j-i>1) store the product and the index j (or i and j) but then we need to combine with later pairs.
        # But note: the subsequence is (p, q, r, s) with p < q < r < s and q-p>1, r-q>1, s-r>1. So, the two pairs are (p, r) and (q, s) but note that q must be between p and r, and s between r and the end.
        # Actually, we can break the subsequence into two pairs: (p, q) and (r, s) but that doesn't directly help. Alternatively, we can consider the middle two indices.

        # Another idea: for each index r (which will be the third element in the subsequence), we can look for pairs (p, r) and (q, s) such that p < q < r < s and the product condition holds. But then we need to count the pairs (p, q) and (r, s) separately.

        # Alternatively, we can use a two-pointer or dynamic programming approach, but the condition is multiplicative.

        # Let me think differently: we can use a dictionary to store the product of pairs (i, j) (with i < j and j-i>1) and then for each subsequent pair (k, l) (with k > j and l > k and l-k>1) we check if the product is the same. But that is O(n^4).

        # We need to optimize. We can precompute all pairs (i, j) with j-i>1 and store the product and the indices. Then, for each pair (i, j), we can look for another pair (k, l) with k > j and l > k and l-k>1 such that nums[i]*nums[k] == nums[j]*nums[l] (if we consider the condition as nums[i]*nums[k] == nums[j]*nums[l] for the subsequence (i, j, k, l)). But wait, the condition is nums[p]*nums[r] == nums[q]*nums[s]. So, if we fix r (which is k in this case), then we need to find p and q such that p < q < r and then s such that s > r and the product condition holds.

        # Actually, we can fix the middle two indices. But that might not help.

        # Another idea: use a dictionary to store the product of pairs (i, j) (with i < j and j-i>1) and then for each subsequent index, update the dictionary. But then we need to combine pairs from different parts.

        # Alternatively, we can use a two-layer approach: for each index r (as the third element), we can consider all pairs (p, q) with p < q < r and then for each s > r, check the condition. But that is O(n^3).

        # Given n=1000, O(n^3) is 1e9, which might be acceptable in Pyton in C++ but in Python it might be borderline. But let's see if we can do better.

        # Actually, we can use a dictionary to store the pairs (i, j) (with i < j and j-i>1) and then for each new index, we can update the dictionary and then combine with previous pairs. But the condition requires the indices to be strictly increasing and with gaps.

        # Let me try a different perspective: we can iterate over the array and for each element, consider it as the third element (r) in the subsequence. Then, for each r, we can look for pairs (p, q) such that p < q < r and q-p>1, and then for each such pair, we can look for an s (s > r) such that nums[s] = nums[p] * nums[r] / nums[q]. But we have to avoid division and use multiplication.

        # Actually, the condition is nums[p]*nums[r] == nums[q]*nums[s]. So, for fixed p, q, r, we can compute the required nums[s] = (nums[p]*nums[r]) / nums[q]. But since we're dealing with integers, we can check if (nums[p]*nums[r]) is divisible by nums[q] and then check if that value exists in the future.

        # But then, we need to count the number of s (with s > r