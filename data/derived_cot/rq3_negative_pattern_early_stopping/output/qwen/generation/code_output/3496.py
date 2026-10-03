import math
from typing import List

class Solution:
    def minNumberOfSeconds(self, mountainHeight: int, workerTimes: List[int]) -> int:
        lo, hi = 0, 10**15
        
        def total_reduction(T):
            total = 0