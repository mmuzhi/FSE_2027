class Solution:
    def countValidSelections(self, nums: List[int]) -> int:
        n = len(nums)
        zeros = [i for i, x in enumerate(nums) if x == 0]
        count = 0
        for start in zeros:
            for direction in [1, -1]:
                arr = nums.copy()
                curr = start
                d = direction
                # We'll simulate until we go out of bounds
                while 0 <= curr < n:
                    if arr[curr] == 0:
                        curr += d
                    else:
                        arr[curr] -= 1
                        d *= -1
                        curr += d
                # After simulation, check if all zeros
                if all(x == 0 for x in arr):
                    count += 1
        return count