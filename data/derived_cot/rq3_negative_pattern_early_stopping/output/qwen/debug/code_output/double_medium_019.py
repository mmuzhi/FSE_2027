class Solution:
    def corpFlightBookings(self, bookings: List[List[int]], n: int) -> List[int]:
        # We'll create an array of zeros with length n+2 (indices 0 to n+1)
        arr = [0] * (n+2)
        for lv, ar, seats in bookings:
            arr[lv-1] += seats
            arr[ar] -= seats
        
        # Now, we want to compute the prefix sum for the first n elements (indices 0 to n-1)
        # But note: the prefix sum at index i (0-indexed) is the total for flight i+1.
        # We can use itertools.accumulate, but note that the problem does not require to import anything.
        # Alternatively, we can do a loop.

        # Since the problem does not specify if we can use itertools, and to keep it simple, we can do:

        # Let's create an array for the result of length n
        res = [0] * n
        current = 0
        for i in range(n):
            current += arr[i]
            res[i] = current
        
        return res