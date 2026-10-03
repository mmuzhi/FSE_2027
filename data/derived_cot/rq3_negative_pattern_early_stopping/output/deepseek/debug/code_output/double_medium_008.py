from typing import List
from itertools import accumulate

class Solution:
    def corpFlightBookings(self, bookings: List[List[int]], n: int) -> List[int]:
        arr = [0] * (n + 2)
        for first, last, seats in bookings:
            arr[first] += seats
            arr[last + 1] -= seats
        return list(accumulate(arr[1:n+1]))