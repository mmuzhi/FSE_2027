class Solution:
    def minOperations(self, nums: List[int]) -> int:
        n = len(nums)
        # If the array is already non-decreasing, return 0
        if all(nums[i] <= nums[i+1] for i in range(n-1)):
            return 0
        
        # Precompute the greatest proper divisor for numbers up to 10^6
        max_val = max(nums)
        # If max_val is 1, then no operation is needed because 1 is already the smallest
        if max_val == 1:
            return 0
        
        # Create an array to store the greatest proper divisor for numbers from 0 to max_val
        # We'll use a sieve-like method
        gpd = list(range(max_val + 1))  # gpd[i] will store the greatest proper divisor of i
        # For each number, we can mark its multiples
        for i in range(2, max_val + 1):
            if gpd[i] == i:  # i is prime, then its greatest proper divisor is i itself? No, wait, for prime, the greatest proper divisor is 1.
                # Actually, we need to set gpd[i] to 1 for primes, but we'll do that by marking multiples
                continue
            # Instead, we can set gpd for multiples of i
            # But a better way is to use a sieve to record the smallest prime factor, then derive the greatest proper divisor
            # Alternatively, we can iterate and for each composite number, set gpd to the number divided by its smallest prime factor
            # But let's do a simpler method: for each i, we can set gpd[i] = i // p, where p is the smallest prime factor of i.
            # But we don't have the smallest prime factor. Let's change the approach.
            # We'll create an array for smallest prime factor (spf) first.
        
        # Let's use a sieve to compute the smallest prime factor (spf)
        spf = list(range(max_val + 1))  # spf[i] = smallest prime factor of i
        for i in range(2, int(max_val**0.5) + 1):
            if spf[i] == i:  # i is prime
                for j in range(i*i, max_val+1, i):
                    if spf[j] == j:
                        spf[j] = i
        
        # Now, for each number i, the greatest proper divisor is i // spf[i]
        # But note: if i is prime, then spf[i] is i, so i//i = 1, which is correct.
        # However, for composite numbers, we can get the greatest proper divisor by dividing by the smallest prime factor and then taking the maximum divisor? Actually, the greatest proper divisor is the number divided by its smallest prime factor, but only if the number is composite. For primes, it's 1.
        # Actually, the greatest proper divisor of a number i is i divided by its smallest prime factor. Because the smallest prime factor gives the largest quotient when dividing.
        # Example: 25, smallest prime factor is 5, 25//5=5. For 12, smallest prime factor is 2, 12//2=6, which is the greatest proper divisor. For 9, smallest prime factor is 3, 9//3=3, which is correct. For 4, smallest prime factor is 2, 4//2=2, correct. For 1, no divisor, but our array elements are at least 1, and 1 has no proper divisor, so we don't need to handle 1 separately because the operation is not defined for 1? Actually, the problem says positive divisor strictly less than x. For 1, there is no such divisor, so we cannot perform the operation on 1. But note the constraint: nums[i] >= 1. So if we have 1, we cannot change it. 

        # But wait, the operation is defined only for numbers that have a proper divisor. So for 1, we cannot perform the operation. Therefore, if the array contains 1 and we need to change a number that is 1, it's impossible. However, the problem says "any number of times", but if we cannot change a 1, then we must leave it. 

        # However, note that the operation is allowed on any element. But if the element is 1, then there is no proper divisor, so the operation is not defined. Therefore, we cannot change 1. 

        # So, if there is a 1 in the array, then we cannot change it. Therefore, if the array is not non-decreasing and we have a 1 that is causing a