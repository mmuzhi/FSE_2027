class Solution:
    def maxValue(self, nums: List[int], k: int) -> int:
        n = len(nums)
        # We'll use bit masks and dynamic programming or two pointers? 
        # Since the numbers are small (up to 127) and the array is 400, we can try to use meet-in-middle or state space search with bit masks.

        # Alternatively, note that the OR operation is monotonic: adding more numbers can only set more bits. 
        # We need to choose two sets of k numbers. The OR of a set is the union of bits from all numbers in the set.

        # The maximum value of the XOR is achieved when the two ORs are as different as possible. 

        # We can consider that the OR of the first half and the OR of the second half are two numbers (each up to 127) and we want to maximize their XOR.

        # But note: the two sets are chosen from the same array without replacement.

        # We can use a DP approach where we consider the ORs of the two halves. But the state space is 2^7 * 2^7, which is 128*128=16384, and we have to choose two sets of k from 400, which is too big.

        # Alternatively, we can use a different approach: since the numbers are small (7 bits), we can use a trie (binary trie) for the ORs.

        # But wait, the problem is similar to "Maximum XOR for Two Subsets of Fixed Size" but with OR instead of the numbers themselves.

        # Let me reframe: We need to split the array into two groups of size k (but actually, we are choosing a subsequence of 2*k, so two groups of k, but the groups are not necessarily contiguous and the order in the subsequence is the order of appearance).

        # Actually, the problem is: choose 2*k indices (in increasing order) and split them into two halves: the first k and the last k. Then compute the OR of the first half and the OR of the second half, then XOR them.

        # We can use a two-step approach: first, choose 2*k indices, then split them into two halves. But the order of the subsequence is fixed (the original order). So the two halves are the first k and the last k of the chosen 2*k elements.

        # So we need to choose 2*k indices from the array (in increasing order) and then the first k and last k are fixed by the order.

        # This is a combinatorial problem. But 400 choose 2*k is too big.

        # We need to use dynamic programming with state (i, a, b) where i is the current index, a is the OR of the first half, b is the OR of the second half? But then we have to track which numbers are in the first half and which in the second half, and we have to assign exactly k to each.

        # Alternatively, we can use a different idea: the maximum value of the expression is the maximum XOR of two numbers, each being the OR of a set of k numbers from the array. But note, the two sets must be disjoint and together form a subsequence (so the indices must be increasing).

        # But note: the two sets are consecutive in the subsequence, but the subsequence is not necessarily contiguous. However, the two sets are the first k and the last k of the chosen 2*k elements. So the two sets are disjoint and the elements of the first set must all appear before the elements of the second set in the original array.

        # So the problem reduces to: choose two disjoint sets A and B, each of size k, such that all elements of A appear before all elements of B in the original array (when we pick the subsequence, the order is preserved). Then compute (OR of A) XOR (OR of B) and maximize that.

        # Now, the array length is 400, and k is at most 200. We cannot iterate over all subsets.

        # Another idea: use bit masks and meet-in-middle. But the numbers are small (7 bits) so the OR of any set can be represented in 7 bits. There are at most 128 possible OR values.

        # We can precompute for each possible OR value, the minimum index (or the earliest occurrence) needed to achieve that OR. But that might not be straightforward.

        # Alternatively, we can use a DP that goes over the array and for each position, we track the OR of the first half and the OR of the second half, but that state space is 128*128 and we have 400 positions, so 400*1