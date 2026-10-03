from collections import deque

class Solution:
    def sequentialDigits(self, low, high):
        out = []
        queue = deque(range(1,10))
        while queue:
            elem = queue.popleft()
            if low <= elem <= high:
                out.append(elem)
            last_digit = elem % 10
            if last_digit < 9:
                new_elem = elem * 10 + (last_digit + 1)
                queue.append(new_elem)
        return out