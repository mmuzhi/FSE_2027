import sys
from collections import defaultdict

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    
    it = iter(data)
    n = int(next(it)); W = int(next(it))
    blocks = []
    for i in range(n):
        x = int(next(it)); y = int(next(it))
        blocks.append((x, y))
        
    q = int(next(it))
    queries = []
    for i in range(q):
        t = int(next(it)); a = int(next(it))
        queries.append((t, a))
        
    # We'll map block index (from 1 to N) to its initial (x, y)
    # But note: the queries ask for a block by its index (A_j). We need to track the block's movement.

    # However, note: the movement is deterministic and depends on the entire system.

    # We need to determine for a block (x0, y0) at time T: 
    #   How many times has it been moved? And has it been removed?

    # But note: removals happen only when the entire bottom row is filled. And the falling is one row per time step (if not blocked).

    # Let's define:
    #   Let g = 0 (ground level, initially row 1 is the bottom, so ground is at row 0 meaning the bottom row is row 1)
    #   But we can think of the ground as the current bottom row (which is row 1 initially). Then, when the entire bottom row is filled, we remove it and the ground moves to row 2.

    # However, the falling is not just one row per time step because of the removals.

    # Alternatively, we can think of the entire process as:

    #   Each block falls until it hits a block or the ground. Then, if the entire bottom row (current ground+1) is filled, the ground moves up.

    # But note: the removal condition is checked at the beginning of each time step, and then the falling step is done.

    # We can model the system by tracking the minimum row (from the bottom) that each column has a block. But note: the grid has W columns.

    # However, the constraints are high (N, W up to 200000) and T up to 10^9.

    # Another idea: 

    #   The entire system can be seen as a set of columns. In each column, the blocks fall one by one, but the falling is blocked by the next block in the same column.

    #   But the removal condition is global: the entire bottom row must be filled. 

    #   The falling of a block in a column is independent of other columns, except for the removal condition.

    #   The removal condition requires that in the current bottom row (say row r), every column has a block. Then, that row is removed and the ground moves up.

    #   The falling of a block is: it falls one row per time step, unless there is a block in the cell below (or the entire bottom row is filled and then the block falls further).

    #   But note: the falling step is done for all blocks at once (from bottom to top) and the removal condition is checked at the beginning.

    #   We can compute the final position of a block by:

    #   Let f(x) be the number of blocks in column x (initially). Then, the blocks in a column fall one by one. The lowest block in a column will fall until it hits the ground or a block. Then, the next block in the same column will fall until it hits the block below or the ground.

    #   But the removal condition: the entire bottom row must be filled. This means that the ground can rise only if every column has a block at the current ground level.

    #   The process is similar to a "multi-brick" falling with a global condition.

    #   We can compute the ground level (g) after T time steps? But T can be up to 10^9.

    #   Alternatively, we can compute for each block the time when it is removed (if ever) and its position at time T.

    #   However, note: the removal condition is global and the falling is sequential.

    #   Let's define:
    #       Let g = 0 (ground level, meaning the bottom row is row 1, so the ground is at row 0)
    #       Then, the current bottom row is g+1.

    #   But note: the initial state: the blocks are at (x, y). We can transform the coordinates: let y' = (initial row from bottom) = Y_i. Then, the ground is initially at 0, so the bottom row is 1.

    #