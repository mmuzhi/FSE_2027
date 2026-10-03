class Solution:
    def sortMatrix(self, grid: List[List[int]]) -> List[List[int]]:
        n = len(grid)
        d_values = {}
        for i in range(n):
            for j in range(n):
                d = i - j
                if d not in d_values:
                    d_values[d] = []
                d_values[d].append((i, j, grid[i][j]))
        
        ans = [[0] * n for _ in range(n)]
        for d, lst in d_values.items():
            sorted_lst = sorted(lst, key=lambda x: x[0])
            values = [x[2] for x in sorted_lst]
            if d >= 0:
                values.sort(reverse=True)
            else:
                values.sort()
            for idx, (i, j, _) in enumerate(sorted_lst):
                ans[i][j] = values[idx]
        return ans