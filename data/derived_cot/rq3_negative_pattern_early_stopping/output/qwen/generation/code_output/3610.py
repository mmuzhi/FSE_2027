from collections import Counter

class Solution:
    def findXSum(self, nums: List[int], k: int, x: int) -> List[int]:
        n = len(nums)
        result = []
        # Iterate over each starting index of the window
        for i in range(n - k + 1):
            window = nums[i:i+k]
            # Count frequencies
            freq = Counter(window)
            # Create a list of (count, num) for each distinct element
            freq_list = [(count, num) for num, count in freq.items()]
            # Sort by count descending, then by num descending
            freq_list.sort(key=lambda a: (-a[0], -a[1]))
            # Take the top x elements
            top_x = freq_list[:x]
            # Calculate the sum of the kept elements
            s = 0
            for count, num in top_x:
                s += count * num
            result.append(s)
        return result