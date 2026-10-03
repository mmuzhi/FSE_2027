class Solution:
    def subsequencesWithMiddleMode(self, nums: List[int]) -> int:
        mod = 10**9 + 7
        n = len(nums)
        ans = 0
        
        # Precompute combinations for two from a multiset? But we need to consider the counts of each number in left and right.
        # Instead, we can iterate over each index as the middle.
        # For each index i, we consider nums[i] as the middle element.
        # Then, we need to count the number of ways to choose two from the left (indices < i) and two from the right (indices > i) such that the total frequency of nums[i] in the subsequence is strictly greater than the frequency of any other element.
        # But note: the condition is equivalent to: the total frequency of nums[i] (which is 1 + count_left + count_right) must be at least 3 (because if it's 3, then no other element can appear 3 or more, but since the subsequence is only 5, the maximum other element can appear is 2). So, we need 1 + count_left + count_right >= 3, i.e., count_left + count_right >= 2.
        # But wait, that's not sufficient. We must also ensure that no other element appears 3 or more times. But since the subsequence is only 5, the maximum any other element can appear is 2 (if we choose two of the same from left or right). So, if the middle element appears at least 3 times, then it is the unique mode. But if it appears only 2 times (so total 2), then we must ensure that no other element appears 2 times. But if we choose two of the same from left or right, then that element would appear 2 times, which is not less than 2 (the middle element's count). So, in that case, the condition fails. Therefore, the middle element must appear at least 3 times in the subsequence (i.e., 1 (middle) + at least 2 from left or right) to be the unique mode.

        # Actually, the condition is: the middle element must appear more times than any other element. So, if the middle element appears 3 times, then no other element can appear 3 or more. But in a subsequence of 5, the maximum any element can appear is 5. But the other elements can appear at most 2 (if we choose two of the same from left or right). So, if the middle element appears 3, 4, or 5 times, then it is the unique mode.

        # Therefore, for a fixed middle element (at index i) with value x, we need to choose two from the left and two from the right such that the total count of x is at least 3. But note: the two left and two right can include x's. So, we can break the left and right into counts of x and other numbers.

        # Let's define:
        #   left_counts: frequency of each number in the left part (indices < i)
        #   right_counts: frequency of each number in the right part (indices > i)

        # But note: the left part and right part are fixed for each i.

        # Then, the total count of x in the subsequence is: 1 (middle) + (number of x chosen from left) + (number of x chosen from right). The number of x chosen from left can be 0, 1, or 2 (if there are at least two x's in the left). Similarly for the right.

        # We need: 1 + (left_x_count) + (right_x_count) >= 3, i.e., left_x_count + right_x_count >= 2.

        # But also, we must ensure that no other element appears 3 or more times. But since the maximum any other element can appear is 2 (because we are only choosing two from left and two from right, and the middle is x, so for an element y != x, the maximum it can appear is 2 (if we choose two y's from left or two from right, or one from left and one from right). So, the condition is automatically satisfied if the middle element appears at least 3 times.

        # Therefore, the condition reduces to: the total count of x (middle element) in the subsequence must be at least 3.

        # Then, the problem becomes: for each index i, count the number of ways to choose two from the left (from the multiset of left elements) and two from the right (from the multiset of right elements) such that the total count of x (the middle element) is at least 3.

        # But note: the two left elements and two right