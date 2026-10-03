class Solution:
    def countArrays(self, original: List[int], bounds: List[List[int]]) -> int:
        n = len(original)
        # Calculate the cumulative effect: for each i, the value of copy[i] is original[i] + (x - original[0])
        # So, for each i, we have: bounds[i][0] <= original[i] + (x - original[0]) <= bounds[i][1]
        # Rearranged: bounds[i][0] - original[i] + original[0] <= x <= bounds[i][1] - original[i] + original[0]
        # We'll compute the lower and upper bounds for x from each index.
        low = []
        high = []
        for i in range(n):
            # For each index i, the constraint on x is:
            # x >= bounds[i][0] - original[i] + original[0]
            # x <= bounds[i][1] - original[i] + original[0]
            low_bound = bounds[i][0] - original[i] + original[0]
            high_bound = bounds[i][1] - original[i] + original[0]
            low.append(low_bound)
            high.append(high_bound)
        
        # Now, we need to find the intersection of all these intervals for x.
        # The overall x must be in [max(low), min(high)] (if the intersection is non-empty)
        x_low = max(low)
        x_high = min(high)
        
        # If there's no intersection, return 0.
        if x_low > x_high:
            return 0
        
        # The number of integer x in the interval [x_low, x_high] is (x_high - x_low + 1)
        return x_high - x_low + 1