import sys

def main():
    data = sys.stdin.read().splitlines()
    if not data:
        return
    n = int(data[0].strip())
    grid = []
    for i in range(1, 1+n):
        grid.append(list(data[i].strip()))
    
    # We'll perform the operations for i from 0 to n//2 - 1
    # For each i, we consider the layer from i to n-1-i (inclusive)
    # For each (x, y) in [i, n-1-i] x [i, n-1-i], set grid[y][n-1-x] to grid[x][y] (using the grid from the start of the operation)
    # But note: the operation is done sequentially for each i, and each operation uses the grid from the previous operation.
    # However, the problem says to perform the operations for i=1,2,...,N/2 in order, and for each i, for all pairs (x,y) in [i, N+1-i] (1-indexed) set (y, N+1-x) to (x,y).
    # We are using 0-indexed, so for i (0-indexed) from 0 to n//2 - 1, and for x from i to n-1-i, and y from i to n-1-i, set grid[y][n-1-x] = grid[x][y] (but using the grid from the start of the operation for this i).
    #
    # But note: the operation is simultaneous, so we must use the grid from the beginning of the operation for all changes.
    #
    # However, if we do it in two nested loops, we can create a new grid for the current operation and then assign.
    #
    # Alternatively, we can do the operation for each i without affecting the current grid by using a temporary grid or by processing in a specific order.
    #
    # But note: the operation for i=0 (outermost) uses the original grid. Then for i=1, we use the grid after i=0, etc.
    #
    # We can do:
    #   for i in range(0, n//2):
    #       new_grid = [row[:] for row in grid]   # make a copy of the current grid
    #       for x in range(i, n-i):
    #           for y in range(i, n-i):
    #               # set new_grid[y][n-1-x] to grid[x][y] (the grid at the start of the operation)
    #               # But wait, we are using the grid from the start of the operation, so we should use the original grid for this operation.
    #               # However, we are updating new_grid, but the value we use is from the grid at the start of the operation (which is the grid from the previous operation).
    #               # So we can use the grid from the previous operation (which is stored in grid) to set new_grid[y][n-1-x] = grid[x][y]
    #       grid = new_grid
    #
    # But wait, the operation is defined as: for each (x,y) in the range, set (y, n-1-x) to (x,y). So we are copying from (x,y) to (y, n-1-x). 
    #
    # However, note that (x,y) and (y, n-1-x) are two different cells. And we are doing it for all (x,y) in the range. 
    #
    # But the problem says: "replace the color of cell (y, N + 1 - x) with the color of cell (x, y)". So we are setting (y, n-1-x) to the color of (x,y). 
    #
    # But note: if we do this for all (x,y), then we are effectively reflecting the grid in a specific way. 
    #
    # However, the above approach would set new_grid[y][n-1-x] = grid[x][y]. But note that (x,y) is the source and (y, n-1-x) is the target. 
    #
    # But wait, the operation is defined for all (x,y) in the range. So for example, in the 2x2 example, we set:
    #   (0,0) -> (0,7) for n=8? Wait, no, for n=8, the range for i=0 is from 0 to 7. Then, for (0,0): set (0,7) to grid[0][0]. (0,1): set (1,7) to grid[0][1]. (0,2): set (2,