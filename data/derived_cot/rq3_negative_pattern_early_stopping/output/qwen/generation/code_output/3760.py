class Solution:
    def assignElements(self, groups: List[int], elements: List[int]) -> List[int]:
        if not groups:
            return [-1] * len(elements)
        max_group = max(groups)
        max_element_val = 10**5
        best = [10**9] * (max_element_val + 1)
        for idx, val in enumerate(elements):
            if idx < best[val]:
                best[val] = idx
        
        min_index = [10**9] * (max_group + 1)
        for x in range(1, max_element_val + 1):
            if best[x] != 10**9 and x <= max_group:
                for m in range(x, max_group + 1, x):
                    if best[x] < min_index[m]:
                        min_index[m] = best[x]
        
        res = []
        for size in groups:
            if min_index[size] == 10**9:
                res.append(-1)
            else:
                res.append(min_index[size])
        return res