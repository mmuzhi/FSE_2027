class Solution:
    def sumOfGoodSubsequences(self, nums: List[int]):
        mod = 10**9 + 7
        from collections import defaultdict, deque
        freq = defaultdict(int)
        for num in nums:
            freq[num] += 1
        
        # We'll use DP with two dictionaries: one for the count of subsequences ending with a number, and one for the total sum of such subsequences.
        # But we need to consider the order. Alternatively, we can use a DP that processes numbers in sorted order and use a Fenwick tree or segment tree to handle the transitions, but that might be overkill.

        # Another idea: use DP that iterates over the array and for each element, update the DP state for the next numbers (i.e., numbers that are current+1 and current-1). But then, we have to account for the fact that the subsequence must be in increasing order of indices.

        # Actually, we can use a DP that goes from left to right and for each element, we consider the last element in the subsequence. But the state would be the last element's value, which can be up to 10^5, and we have 10^5 elements, so that's 10^10 states, which is too slow.

        # Alternatively, we can use a DP that uses the value and the index, but that's also too slow.

        # Let me think differently. We can use a DP that is based on the value and the count of subsequences ending with that value, but we must account for the order. However, the condition is about consecutive elements, so the next element must be either value+1 or value-1. But the order is fixed by the array.

        # We can use a two-pass method: first, sort the array by value, but then we lose the original order. So that won't work.

        # Another idea: use a DP that for each element, we store the number of subsequences ending with that element and the total sum of those subsequences. Then, for each element, we look at the elements that are one less or one more and that appeared before it (in the array) and update the current element's DP.

        # But then, we need to update the DP for each element in the order of the array. However, the condition is about consecutive elements in the subsequence, so the next element must be adjacent in value. But the previous element in the subsequence must have been processed already.

        # Steps:
        # 1. We'll iterate over the array from left to right.
        # 2. For each element, we'll consider two cases: 
        #    a) The subsequence that ends with this element and has no previous element (single element).
        #    b) The subsequence that ends with this element and has a previous element that is either one less or one more.
        # 3. We'll maintain two dictionaries: one for the count of subsequences ending with a value, and one for the total sum of subsequences ending with a value.

        # However, the challenge is that the same value might appear multiple times, and we need to account for all occurrences.

        # Let's define:
        # dp_count[x] = number of subsequences ending with x (from the processed part of the array)
        # dp_sum[x] = total sum of all subsequences ending with x

        # Then, for a new element 'v' at index i, we can form new subsequences by:
        #   - Starting a new subsequence with v: count_new = 1, sum_new = v
        #   - Appending v to subsequences ending with v-1: count_from_prev = dp_count.get(v-1, 0), sum_from_prev = dp_sum.get(v-1, 0)
        #   - Appending v to subsequences ending with v+1: count_from_prev = dp_count.get(v+1, 0), sum_from_prev = dp_sum.get(v+1, 0)

        # But wait, the condition is that consecutive elements must differ by 1. So, if we have a subsequence ending with v-1, then adding v (which is (v-1)+1) is allowed. Similarly, a subsequence ending with v+1 can have v (which is (v+1)-1) appended.

        # However, note that the subsequence must be in the original order. But if we are processing from left to right, then the subsequences ending with v-1 or v+1 that we have already processed (i.e., with indices less than the current index) are valid.

        # But the problem: the same value might appear multiple times, and we need to account for all occurrences. Also, the subsequences ending with a value might have been formed by