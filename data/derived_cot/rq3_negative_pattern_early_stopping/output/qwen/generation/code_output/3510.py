class Solution:
    def maximumTotalSum(self, maximumHeight: List[int]) -> int:
        maximumHeight.sort(reverse=True)
        total = 0
        prev = float('inf')
        for h in maximumHeight:
            if h >= prev - 1:
                # We can use the next distinct number which is prev - 1
                total += prev - 1
                prev = prev - 1
            else:
                # If the next distinct number is less than h, then we use h
                total += h
                prev = h - 1
        return total if prev >= 1 else -1