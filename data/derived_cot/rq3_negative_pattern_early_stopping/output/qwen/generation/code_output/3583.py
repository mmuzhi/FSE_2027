class Solution:
    def gcdValues(self, nums: List[int], queries: List[int]) -> List[int]:
        from collections import Counter
        import math
        from functools import lru_cache
        
        n = len(nums)
        cnt = Counter(nums)
        max_val = max(nums) if nums else 0
        
        # Precompute the frequency of divisors for each number
        # But we need to count the pairs that have a particular GCD
        # Alternatively, we can use the method of counting pairs with gcd divisible by d
        # Then use Möbius inversion to get the exact counts for each gcd value
        
        # Step 1: Precompute the frequency of each number
        # Step 2: For each divisor d, count the numbers divisible by d
        # Then, the number of pairs with gcd exactly d can be computed using inclusion-exclusion
        
        # But note: We are only interested in the sorted list of gcd values, not the exact counts for each distinct gcd?
        # Actually, we need to know the k-th smallest gcd value. So we need to know the cumulative counts for each gcd value.
        
        # Alternatively, we can use a method that counts the number of pairs with gcd >= d and then use that to find the k-th smallest.
        # But that might be complex.
        
        # Another idea: use the fact that the gcd of two numbers is the same as the gcd of their divisor sets.
        # We can use a frequency array for divisors and then use a two-pointer or something similar.
        
        # Actually, there's a known approach for this problem: 
        # 1. Count the frequency of each number.
        # 2. For each divisor d (from 1 to max_val), count the numbers divisible by d.
        # 3. Then, the number of pairs (i, j) such that d divides gcd(i, j) is C(count[d], 2).
        # 4. Then, using Möbius function, we can compute the exact count for gcd exactly d.
        # But then, we need to reconstruct the sorted list of gcds. But the total number of distinct gcds might be too many to list individually.
        
        # Alternatively, we can use a different approach: 
        # Instead of listing all gcds, we can use a "next pointer" method to iterate over the divisors and count the number of gcds <= a certain value.
        # But that might be too slow for 10^5 queries.
        
        # Actually, we can use the following method:
        # Let F(d) be the number of pairs with gcd exactly d.
        # Then, we can compute F(d) for all d by:
        #   Let A[d] = count of numbers divisible by d.
        #   Then, the number of pairs with gcd divisible by d is C(A[d], 2).
        #   Then, F(d) = C(A[d], 2) - sum_{k>=2} F(k*d)
        # But that is recursive and might be heavy.
        
        # Alternatively, we can use the Möbius function:
        #   F(d) = sum_{k>=1} μ(k) * C(A[k*d], 2)
        # But then, we need to know the cumulative counts for each gcd value.
        
        # However, note that the problem asks for the k-th smallest gcd value. So we need to know the distribution of gcds.
        
        # Steps:
        # 1. Precompute the frequency of each number.
        # 2. Precompute the frequency of divisors: for each d, count how many numbers are divisible by d.
        # 3. Precompute the Möbius function for numbers up to max_val.
        # 4. Then, for each d, compute F(d) = number of pairs with gcd exactly d.
        # 5. Then, we can create an array of all gcds? But that would be too many (up to 10^10 pairs).
        # 6. Instead, we can use a Fenwick tree or segment tree to store the cumulative counts for each gcd value, but the gcd values can be up to 50000, and the distinct gcds might be many.
        
        # Actually, we can use a different approach: 
        # We can iterate over divisors and then use a two-pointer to count the number of gcds <= a certain value, but that might be complex.
        
        # Alternatively, we can use the "Mo's algorithm" or offline queries, but that might be overkill.
        
        # Another idea: use the fact that the gcd of two numbers is at most the minimum of the two numbers. But that doesn't help much.
        
        # Let me think about the example: nums = [2,3,4],