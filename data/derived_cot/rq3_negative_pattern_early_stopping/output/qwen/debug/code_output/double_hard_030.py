from collections import defaultdict, deque

class Solution:
    def isTransformable(self, s: str, t: str) -> bool:
        # Build a dictionary mapping each digit to a deque of its indices in s.
        idx = defaultdict(deque)
        for i, c in enumerate(s):
            idx[int(c)].append(i)
        
        cur = -1  # current pointer, initially -1 (before the first character)
        for char in t:
            d = int(char)
            # Remove all indices that are <= cur (we cannot use them because they are before or at the current pointer)
            while idx[d] and idx[d][0] <= cur:
                idx[d].popleft()
            if not idx[d]:
                return False
            # We found a valid index for this digit, update cur to this index
            cur = idx[d].popleft()
        return True