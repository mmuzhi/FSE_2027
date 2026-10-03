from typing import List

class Solution:
    def corpFlightBookings(self, bookings: List[List[int]], n: int) -> List[int]:
        arr = [0] * (n + 2)
        for l, r, seats in bookings:
            arr[l] += seats
            arr[r + 1] -= seats
        
        result = []
        current = 0
        for i in range(1, n + 1):
            current += arr[i]
            result.append(current)
        return result