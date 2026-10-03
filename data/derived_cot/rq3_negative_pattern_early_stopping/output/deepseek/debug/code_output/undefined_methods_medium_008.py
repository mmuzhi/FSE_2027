from typing import List
import itertools

class Solution:
    def corpFlightBookings(self, bookings: List[List[int]], n: int) -> List[int]:
        arr = [0] * (n + 1)
        for first, last, seats in bookings:
            arr[first - 1] += seats
            arr[last] -= seats
        return list(itertools.accumulate(arr[:-1]))