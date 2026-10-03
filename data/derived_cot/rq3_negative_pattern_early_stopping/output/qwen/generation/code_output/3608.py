class Solution:
    def subsequencePairCount(self, nums: List[int]) -> int:
        mod = 10**9 + 7
        n = len(nums)
        # Precompute the divisors for numbers up to 200
        max_val = 200
        divisors = [[] for _ in range(max_val + 1)]
        for i in range(1, max_val + 1):
            for j in range(i, max_val + 1, i):
                divisors[j].append(i)
        
        # Count subsequences with gcd exactly d for each divisor d
        # We'll use a DP where dp[i][d] = number of ways to choose a subsequence from the first i numbers with gcd d
        # But we need to do it for the entire array and then combine two disjoint subsequences.
        # Alternatively, we can use the idea: for each divisor d, count the number of subsequences (from the entire array) with gcd divisible by d, then use Möbius inversion to get the exact count.
        # But then, how to count pairs of disjoint subsequences with the same gcd?
        # Another idea: iterate over all pairs of indices and assign each index to one of three sets: S, T, or none. But that's 3^n, which is too slow for n=200.

        # Alternatively, we can use the following approach:
        # Let F(d) be the number of non-empty subsequences (from the entire array) with gcd exactly d.
        # Then, the total number of pairs (S, T) with gcd(S)=gcd(T)=d is F(d) * F(d) but then subtract the cases where S and T share indices? But wait, the subsequences must be disjoint. So, we cannot simply square F(d) because the subsequences might overlap.

        # Actually, the problem requires disjointness. So, we need to count pairs (S, T) such that S and T are disjoint and gcd(S)=gcd(T)=d.

        # We can use the following: for each divisor d, we can count the number of ways to assign each index to one of three categories: S, T, or none, such that the gcd of S is d and the gcd of T is d, and both S and T are non-empty.

        # But that is still too slow.

        # Another idea: use the fact that the array is small (n=200) but the numbers are small (up to 200). We can use a two-dimensional DP that considers the gcd of the first subsequence and the gcd of the second subsequence, but then we have to account for disjointness.

        # Alternatively, we can use the following method:
        # 1. Precompute for each divisor d, the list of indices that are divisible by d (or rather, the numbers that are divisible by d) but that doesn't directly help.

        # Let me think differently. We can use the principle of inclusion-exclusion and the fact that the GCD of a subsequence is determined by the prime factors.

        # But perhaps a better idea is to use the following:

        # Let A be the set of all non-empty subsequences. We want to count pairs (S, T) such that S and T are disjoint and gcd(S)=gcd(T).

        # We can fix the gcd value, say d. Then, we need to count the number of ways to choose two disjoint non-empty subsequences (S, T) such that gcd(S)=d and gcd(T)=d.

        # But note: the subsequences must have gcd exactly d, not a multiple of d.

        # We can use the following: for each divisor d, let F(d) be the number of non-empty subsequences (from the entire array) with gcd exactly d. Then, the total number of pairs (S, T) with gcd(S)=gcd(T)=d is the sum over all ways to split the array into three parts: S, T, and the rest, such that S has gcd d and T has gcd d.

        # But how to compute that without iterating over all subsets?

        # Another idea: use the complement. The total number of ways to assign each index to S, T, or neither is 3^n. Then, we can subtract the cases where S or T is empty, and then use inclusion-exclusion for the gcd condition.

        # But that seems messy.

        # Let me look for similar problems. I recall a problem where we count the number of pairs of disjoint subsequences with the same GCD. One common approach is to use a two-pointer or a DP that iterates over the array and keeps track of the gcd of the first subsequence and the gcd of the second subsequence, but that would be O(n * 2^(2*k)) which is too slow.