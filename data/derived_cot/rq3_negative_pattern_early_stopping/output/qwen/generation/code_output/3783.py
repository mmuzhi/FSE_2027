class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        # Total numbers: 1 to n
        # Count of odd numbers: (n+1)//2, even: n//2
        odd_total = (n + 1) // 2
        even_total = n // 2
        
        # We'll use memoization for DP: (pos, last_parity, odd_remaining, even_remaining)
        # last_parity: 0 for even, 1 for odd, and for the first element, we can set last_parity to -1 (meaning none)
        from functools import lru_cache
        
        @lru_cache(maxsize=None)
        def dp(pos, last_parity, odd_remaining, even_remaining):
            # If we have placed all numbers, return 1
            if pos == n:
                return 1
            # If no numbers left, return 0
            if odd_remaining == 0 and even_remaining == 0:
                return 0
            # Determine the required parity for the next element
            if last_parity == 0:  # last was even, so next must be odd
                if odd_remaining == 0:
                    return 0
                ways = 0
                # Choose each available odd number