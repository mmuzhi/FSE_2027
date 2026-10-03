class Solution:
    def findMaxSum(self, nums1: List[int], nums2: List[int], k: int) -> List[int]:
        # Combine the two arrays
        arr = [(a, b) for a, b in zip(nums1, nums2)]
        # Sort by nums1
        arr.sort(key=lambda x: x[0])
        # Group by nums1 value
        from itertools import groupby
        groups = []
        for key, g in groupby(arr, key=lambda x: x[0]):
            groups.append(list(g))
        
        # We'll maintain a min-heap for the top k values from previous groups
        import heapq
        heap = []  # min-heap for the top k values (we'll store negative values to simulate max-heap)
        # But actually, we need to store the actual values and then pop the smallest when we have more than k
        # Alternatively, we can use a min-heap to keep the k largest values. We'll store the negative of the values to use a min-heap as a max-heap for the top k.
        # But actually, we can use a min-heap of size k, but then we need to be able to get the sum of the top k. Alternatively, we can store all the values and then use a sorted list, but that would be O(n) per query.

        # Actually, we can use a min-heap to keep the k largest values. We'll store the negative of the values so that the smallest in the heap is the largest value (in absolute terms). Then, the sum is the negative of the sum of the heap.

        # But we need to add all the values from the previous groups. Actually, we can do:

        # We'll process each distinct value in increasing order. For each distinct value, we have a list of nums2 values from that group. Then, we add those values to the data structure. Then, for the next distinct value, we use the data structure to compute the answer for each index in that next group.

        # But wait, the condition for an index i is: the set of j with nums1[j] < nums1[i]. So for a group with value x, the set of j is all indices with nums1 < x. So we need to have processed all groups with value less than x.

        # So we can do:

        # 1. Sort the entire array by nums1.
        # 2. Then, for each distinct value (in increasing order), we first compute the answer for each index in that group (using the current data structure, which contains all nums2 from groups with nums1 < current). Then, we add the nums2 values from the current group to the data structure.

        # But then, the answer for the current group is computed from the data structure that does not include the current group's nums2 values. That is correct.

        # Steps:

        # - Sort the array by nums1.
        # - Use a min-heap (for the top k values) and a variable to track the current sum of the heap (or we can store the heap and then the sum separately).
        # - Actually, we can maintain a min-heap (for the k largest values) and a variable `current_sum` which is the sum of the heap. Then, for each group (with value x), we first compute the answer for each index in that group: the answer is the current_sum (if we have at least k values, otherwise current_sum is the sum of all). But wait, the data structure (the heap) contains all the nums2 values from groups with nums1 < x. But we only keep the top k in the heap? Actually, we need to keep all the values from previous groups? No, because we are only allowed to choose at most k from the entire set. So we need to know the top k from the entire set of previous groups.

        # But if we keep a min-heap of size k, then we can only get the top k. But the set of previous groups might have more than k values, so we need to keep the top k from the entire set.

        # Actually, we can do:

        #   We maintain a min-heap (for the k largest values from the entire set of previous groups). We also maintain a variable `total` which is the sum of the heap (if the heap has less than k, then we have all the values from previous groups, but we don't need to keep a heap then).

        # But if we keep a min-heap of size k, then we can only get the top k. But the condition is: choose at most k values from the entire set (which is the union of all previous groups). So we need the top k from the entire set.

        # We can use a min-heap to store the k largest values.