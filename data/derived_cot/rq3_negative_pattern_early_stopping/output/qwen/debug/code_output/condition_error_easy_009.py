class Solution:
    def canPlaceFlowers(self, flowerbed: List[int], n: int) -> bool:
        for i in range(len(flowerbed)):
            # Check if we can plant at position i
            if flowerbed[i] == 0:
                # Check left neighbor (if exists)
                left_empty = True if i == 0 else flowerbed[i-1] == 0
                # Check right neighbor (if exists)
                right_empty = True if i == len(flowerbed)-1 else flowerbed[i+1] == 0
                if left_empty and right_empty:
                    flowerbed[i] = 1
                    n -= 1
                    if n <= 0:
                        return True
        return n <= 0