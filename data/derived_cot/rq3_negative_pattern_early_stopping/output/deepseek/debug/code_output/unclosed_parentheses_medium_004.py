from typing import List
from collections import defaultdict

class Solution:
    def numOfPairs(self, nums: List[str], target: str) -> int:
        freq = defaultdict(int)
        for s in nums:
            freq[s] += 1

        pairs = 0
        n = len(target)
        for i in range(1, n):  # split point after i chars
            left = target[:i]
            right = target[i:]
            if left in freq and right in freq:
                cnt_left = freq[left]
                cnt_right = freq[right]
                if left != right:
                    pairs += cnt_left * cnt_right
                else:
                    pairs += cnt_left * (cnt_left - 1)
        return pairs