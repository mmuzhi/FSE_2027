class Solution:
    def maxLength(self, nums: List[int]) -> int:
        exp_map = {
            1: [0, 0, 0, 0],
            2: [1, 0, 0, 0],
            3: [0, 1, 0, 0],
            4: [2, 0, 0, 0],
            5: [0, 0, 1, 0],
            6: [1, 1, 0, 0],
            7: [0, 0, 0, 1],
            8: [3, 0, 0, 0],
            9: [0, 2, 0, 0],
            10: [1, 0, 0, 1]
        }
        n = len(nums)
        max_len = 0
        for start in range(n):
            min_vals = [10**9] * 4
            max_vals = [0] * 4
            total_vals = [0] * 4
            exp_first = exp_map[nums[start]]
            for j in range(4):
                min_vals[j] = exp_first[j]
                max_vals[j] = exp_first[j]
                total_vals[j] = exp_first[j]
            current_length = 1
            valid = True
            for j in range(4):
                if min_vals[j] + max_vals[j] != total_vals[j]:
                    valid = False
                    break
            if valid:
                max_len = max(max_len, current_length)
            for end in range(start + 1, n):
                exp_end = exp_map[nums[end]]
                for j in range(4):
                    total_vals[j] += exp_end[j]
                    if exp_end[j] < min_vals[j]:
                        min_vals[j] = exp_end[j]
                    if exp_end[j] > max_vals[j]:
                        max_vals[j] = exp_end[j]
                valid = True
                for j in range(4):
                    if min_vals[j] + max_vals[j] != total_vals[j]:
                        valid = False
                        break
                if valid:
                    max_len = max(max_len, end - start + 1)
        return max_len