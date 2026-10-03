class Solution:
    def maxRemoval(self, nums: List[int], queries: List[List[int]]) -> int:
        n = len(nums)
        total_queries = len(queries)
        # If the maximum value in nums is greater than the total_queries, then even using all queries we cannot cover the maximum requirement, so return -1.
        if max(nums) > total_queries:
            return -1
        
        # Sort queries by their right endpoint
        queries.sort(key=lambda x: x[1])
        
        # We'll use a min-heap to keep track of the left endpoints of the queries that are active (i.e., that start <= current index and end >= current index)
        import heapq
        left_heap = []
        j = 0
        # We'll traverse each index from 0 to n-1
        # We need to cover each index i with nums[i] queries
        # We'll use a greedy approach: for each index i, we'll add all queries that end at i (or more precisely, that end >= i and start <= i) and then use them to cover i.
        # But note: we can use a query only once, and we want to minimize the total queries used, so we use the queries that end earliest first (so that they don't block future indices unnecessarily).
        # Actually, we'll add queries that end at i (or >= i) and then use them to cover the deficit at i and beyond? 

        # Instead, we can use a two-pointer and a min-heap for the left endpoints of the queries that are active (i.e., that start <= i and end >= i). Then, for each index i, we need to have at least nums[i] queries in the active set. But we can use a query only once, so we need to "spend" queries to cover the deficit.

        # Alternatively, we can use a greedy algorithm that uses the queries in increasing order of their right endpoints and then for each index i, we need to have at least nums[i] queries that cover i. We can use a pointer to add queries that end at i and then use a heap to keep the left endpoints of the queries that are active (so that we can later remove them when they expire).

        # Let's reframe: We want to know the minimum number of queries needed to cover each index i with at least nums[i] queries. Then, the answer is total_queries - minimum_queries.

        # We can use a greedy algorithm that goes from left to right and for each index i, we need to cover the deficit (nums[i] - current_coverage). We can use the queries that end at i to cover the deficit at i.

        # Steps for the greedy algorithm:
        # 1. Sort queries by right endpoint (r).
        # 2. Let current_coverage = [0]*n  (but we don't need to store all, we can use a running count and a heap)
        # 3. Use a pointer j for queries (sorted by r) and a min-heap for the left endpoints of the queries that are active (i.e., that start <= i and end >= i). But actually, we don't need the left endpoints, we need to know the count.

        # Actually, we can use a different approach: 
        # We need to cover each index i with at least nums[i] queries. Each query [l, r] can cover indices from l to r. 
        # We can use a greedy algorithm that uses the queries in increasing order of their right endpoints. For each index i, we need to have nums[i] queries covering it. We can use the queries that end at i to cover i. But also, queries that end beyond i can cover i.

        # We can use a two-pointer and a multiset to keep track of the left endpoints of the queries that are active (i.e., that start <= i and end >= i). Then, for each index i, we need to have at least nums[i] queries in the active set. But we can use a query only once, so we need to "spend" queries to cover the deficit.

        # Actually, we can use a greedy algorithm that "pays" for the deficit at each index i by using the queries that end at i. 

        # Let's define:
        #   deficit[i] = nums[i] - (number of queries that cover i and have been used so far)
        # But we don't know which queries to use.

        # Alternatively, we can use a greedy algorithm that uses the queries in increasing order of their right endpoints and then for each index i, we need to have at least nums[i] queries that cover i. We can use a pointer to add queries that end at i and then use a heap to keep the left endpoints of the queries that are active (so that we can later remove them when they expire