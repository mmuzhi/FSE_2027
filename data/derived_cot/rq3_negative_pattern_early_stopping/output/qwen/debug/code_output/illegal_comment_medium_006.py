class Solution:
    def numMagicSquaresInside(self, grid: List[List[int]]) -> int:
        M, N = len(grid), len(grid[0])
        res = 0
        
        def is_magic(arr):
            nums = []
            for row in arr:
                nums.extend(row)
            if len(nums) != 9:
                return False
            if set(nums) != set(range(1, 10)):
                return False
            
            for i in range(3):
                if sum(arr[i]) != 15:
                    return False
            
            for j in range(3):
                col_sum = arr[0][j] + arr[1][j] + arr[2][j]
                if col_sum != 15:
                    return False
            
            if arr[0][0] + arr[1][1] + arr[2][2] != 15:
                return False
            if arr[0][2] + arr[1][1] + arr[2][0] != 15:
                return False
            
            return True
        
        for i in range(M - 2):
            for j in range(N - 2):
                matrix = []
                for x in range(i, i + 3):
                    matrix.append(tuple(grid[x][j:j+3]))
                if is_magic(matrix):
                    res += 1
        
        return res