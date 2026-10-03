class Solution:
    def beautifulSplits(self, nums: List[int]) -> int:
        n = len(nums)
        if n < 3:
            return 0
        
        # Two mods for double hashing
        mod1 = 10**9 + 7
        mod2 = 10**9 + 9
        base = 131
        
        # Precompute hashes and powers for mod1
        h1 = [0] * (n + 1)
        p1 = [1] * (n + 1)
        for i in range(1, n + 1):
            h1[i] = (h1[i - 1] * base + nums[i - 1]) % mod1
            p1[i] = (p1[i - 1] * base) % mod1
        
        # Precompute hashes and powers for mod2
        h2 = [0] * (n + 1)
        p2 = [1] * (n + 1)
        for i in range(1, n + 1):
            h2[i] = (h2[i - 1] * base + nums[i - 1]) % mod2
            p2[i] = (p2[i - 1] * base) % mod2
        
        # Function to get hash for substring [l, r) (0-indexed, l inclusive, r exclusive)
        def get_hash(l, r, h, p, mod):
            res = (h[r] - h[l] * p[r - l]) % mod
            return res
        
        # Condition 1: nums1 is a prefix of nums2
        count = 0
        # i is the length of nums1 (and also the number of elements in nums2 that must match)
        # i must be at least 1 and at most n//2 (because we need i+i <= n)
        for i in range(1, n // 2 + 1):
            # Check if substring [0, i) equals substring [i, i+i)
            hash1_val1 = get_hash(0, i, h1, p1, mod1)
            hash1_val2 = get_hash(i, i + i, h1, p1, mod1)
            hash2_val1 = get_hash(0, i, h2, p2, mod2)
            hash2_val2 = get_hash(i, i + i, h2, p2, mod2)
            if hash1_val1 == hash1_val2 and hash2_val1 == hash2_val2:
                # Condition 1 holds for this i, then all j from i to n-i-1 are valid
                # The number of j is (n - i - 1) - i + 1 = n - 2*i
                count += (n - 2 * i)
        
        # Condition 2: nums2 is a prefix of nums3
        # Now, we iterate over i (length of nums1) and then j (length of nums2) such that j <= (n - i - j) and the substring [i, i+j) equals [i+j, i+j+j)
        # But note: condition 2 is independent and we must not count splits that are already counted by condition 1.
        # However, we are counting condition 1 separately and condition 2 separately and then adding. But if a split satisfies both, we count it twice. 
        # But the problem says "OR", so we need to count each split only once. 
        # But in our method, we are counting condition 1 by i and then adding all j for that i, and condition 2 by iterating over i and j. 
        # We need to avoid double counting. 
        # Alternatively, we can count condition 2 without including splits that satisfy condition 1. But that would require knowing for each (i, j) if condition 1 holds. 
        # But note: condition 1 and condition 2 are independent and a split (i, j) can satisfy both. 
        # We can use a set or a visited matrix, but that would be O(n^2) memory, which is 12.5e6 booleans, which is 100 MB, acceptable in C++ but in Python, we can try to avoid by not counting condition 1 splits in condition 2.

        # But wait, condition 1 is defined by i (and j>=i) and condition 2 is defined by i and j (with j <= (n-i-j)). 
        # Actually, condition 1 and condition 2 are not mutually exclusive. 

        # We can instead count all splits that satisfy condition 1 or condition 2 by:

        #   total = count_condition1 + count