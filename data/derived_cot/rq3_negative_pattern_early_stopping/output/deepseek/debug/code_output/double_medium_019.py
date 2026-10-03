from typing import List
from itertools import accumulate

class Solution:
    def corpFlightBookings(self, bookings: List[List[int]], n: int) -> List[int]:
        arr = [0] * (n + 1)
        for lv, ar, seats in bookings:
            arr[lv - 1] += seats
            arr[ar] -= seats          # correct index: ar (0‑based) not ar+1
        return list(accumulate(arr[:-1]))