from collections import deque

class Solution:
    def sequentialDigits(self, low, high):
        out = []
        queue = deque(range(1, 10))

        while queue:
            num = queue.popleft()

            if num > high:
                continue

            if low <= num <= high:
                out.append(num)

            last = num % 10
            if last < 9:
                queue.append(num * 10 + last + 1)

        return out