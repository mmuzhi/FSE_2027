from typing import List
from itertools import accumulate

class Solution:
    def corpFlightBookings(self, bookings: List[List[int]], n: int) -> List[int]:
        diff = [0] * (n + 2)
        for first, last, seats in bookings:
            diff[first] += seats
            diff[last + 1] -= seats
        return list(accumulate(diff))[1:-1]