class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        n = len(nums)
        # Separate numbers greater than threshold (they are isolated)
        isolated = [x for x in nums if x > threshold]
        small_nums = [x for x in nums if x <= threshold]
        
        # If there are no small numbers, then answer is len(isolated)
        if not small_nums:
            return len(isolated)
        
        # We'll use union-find for small_nums
        parent = list(range(len(small_nums)))
        rank = [0] * len(small_nums)
        
        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
        
        def union(x, y):
            rx = find(x)
            ry = find(y)
            if rx == ry:
                return
            if rank[rx] < rank[ry]:
                parent[rx] = ry
            elif rank[rx] > rank[ry]:
                parent[ry] = rx
            else:
                parent[ry] = rx
                rank[rx] += 1
        
        # Precompute divisors for all numbers up to threshold (since small_nums are <= threshold)
        # But we only need to consider numbers up to threshold for divisors
        # We'll create a list of divisors for each number from 1 to threshold
        max_val = threshold
        divisors = [[] for _ in range(max_val + 1)]
        for i in range(1, max_val + 1):
            for j in range(i, max_val + 1, i):
                divisors[j].append(i)
        
        # Build graph for small_nums: for each number, consider its divisors and then connect to numbers that are multiples of that divisor and satisfy the condition
        # But note: the condition is LCM(a, b) <= threshold, which is (a * b) / gcd(a, b) <= threshold.
        # We can use the divisor d of a, then for each multiple b of d (b in small_nums), check if (a * b) / d <= threshold * (gcd(a, b) / d) ? 
        # Actually, we can use: for a given a and divisor d of a, then for each b in small_nums that is a multiple of d, we can check if (a * b) / gcd(a, b) <= threshold.
        # But gcd(a, b) is at least d, so if (a * b) / d > threshold, then certainly (a * b) / gcd(a, b) > threshold. But if (a * b) / d <= threshold, then it is necessary to check the actual gcd.
        # However, we can optimize by only considering b such that b <= threshold * d / a (since (a * b) / d <= threshold implies b <= threshold * d / a).
        # But then, we must check the actual gcd condition.
        # But note: the condition (a * b) / gcd(a, b) <= threshold is equivalent to a * b <= threshold * gcd(a, b).
        # We can compute gcd(a, b) using math.gcd, but we have to do it for each candidate b, which might be too slow.
        # But the total number of candidates might be limited because threshold is 200000 and a is at least 1, so for each a, the number of b's that are multiples of a divisor d and <= threshold * d / a is limited.
        # However, worst-case, a=1, then d=1, then b can be up to threshold, so 200000 candidates for a=1. And there are up to 10^5 small numbers, so worst-case 10^5 * 200000 = 20e9 checks, which is too slow in Python.
        #
        # We need a better approach.
        #
        # Alternative approach: 
        # Instead of iterating over divisors for each a, we can precompute for each number from 1 to threshold, the list of numbers in small_nums that are multiples of it.
        # Then, for each number a, we can iterate over its divisors d, and then for each b in the list for d that is <= threshold * d / a, we union a and b.
        # But then, we are still doing the same thing.
        #
        # Another idea: 
        # We can use the fact that if two numbers a and b are to be connected, then they must share a common divisor d such that d >= (a * b) / threshold. But that's not helpful.
        #
        # Let me try to think from the perspective of the threshold.