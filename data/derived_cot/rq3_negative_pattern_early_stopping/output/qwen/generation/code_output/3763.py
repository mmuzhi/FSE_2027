class Solution:
    def separateSquares(self, squares: List[List[int]]) -> float:
        # Calculate total area
        total_sum = 0.0
        ys = []
        for x, y, l in squares:
            total_sum += l * l
            ys.append(y)
            ys.append(y + l)
        
        # Set the search boundaries
        low = min(ys)
        high = max(ys)
        
        # If total_sum is zero, return 0.0
        if total_sum == 0:
            return 0.0
        
        # Binary search for the minimal h
        target = total_sum / 2.0
        
        # Helper function to compute total area below h
        def total_below(h):
            res = 0.0
            for x, y, l in squares:
                if h <= y:
                    continue
                if h >= y + l:
                    res += l * l
                else:
                    res += (h - y) * l
            return res
        
        # Binary search
        while high - low > 1e-7:
            mid = (low + high) / 2
            if total_below(mid) < target:
                low = mid
            else:
                high = mid
        
        return low