class Solution:
    def maxPossibleScore(self, start: List[int], d: int) -> int:
        start.sort()
        n = len(start)
        low, high = 0, start[-1] + d - start[0]
        intervals = [(s, s + d) for s in start]
        
        def feasible(X):
            current = -10**18  # a very small number
            for s, e in intervals:
                # The smallest number we can choose from this interval that is >= current + X
                candidate = max(s, current + X)
                if candidate > e:
                    return False
                current = candidate
            return True
        
        while low <= high:
            mid = (low + high) // 2
            if feasible(mid):
                low = mid + 1
            else:
                high = mid - 1
        return high