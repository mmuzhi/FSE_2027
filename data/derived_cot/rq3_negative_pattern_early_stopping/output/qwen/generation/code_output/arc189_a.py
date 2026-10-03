import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1+n]))
    
    # Check if the target grid is achievable from the initial grid.
    # The initial grid is alternating: [1,0,1,0,...]
    # The target grid must be such that the first cell is 1 (if n>=1) or 0 (if n>=1 and alternating) but wait, the initial grid's first cell is 1.
    # However, note: operations can change the grid, but the first cell is never changed by an operation (unless we use it as an end). But if we use the first cell as an end, then it remains 1 (initially) and then if we set a segment starting at the first cell, then the first cell remains 1. But wait, the operation requires that the ends are the same. So if we use the first cell as an end, it must be the same as the other end. But the first cell is 1, so the other end must be 1. Then, the operation sets the segment between to 1. But then, the first cell remains 1.

    # Actually, the first cell is never changed by any operation because the operation only changes cells from l+1 to r-1. So the first cell is always 1 (if n>=1) in the target grid? Or wait, no: the operation can use the first cell as an end, but it doesn't change it. But the target grid might have a 0 at the first cell? Then, it's impossible.

    # Let me check the sample: 
    # Sample Input 1: N=6, A = [1,1,1,1,1,0]
    # The first cell is 1, which matches the initial grid.

    # Sample Input 2: N=10, A = [1,1,1,1,1,0,1,1,1,0]
    # The first cell is 1, which matches.

    # But what if the target grid has a 0 at the first cell? Then, it's impossible because the first cell is never changed.

    # Similarly, the last cell: if the target grid's last cell is 0, then it must be that the initial grid's last cell is 0 (if n is even) or 1 (if n is odd). But wait, the initial grid is alternating: cell i has i mod 2. So the last cell (n) has n mod 2.

    # Therefore, the target grid must have the first cell equal to 1 (if n>=1) and the last cell equal to n mod 2? Or wait, no: the operations can change the last cell if we use it as an end? Actually, no: the operation only changes the cells between l and r. So the last cell is never changed by an operation. Therefore, the last cell must be the same as the initial grid's last cell.

    # So, necessary conditions for the target grid:
    # 1. The first cell must be 1 (if n>=1) because the initial grid's first cell is 1 and it's never changed.
    # 2. The last cell must be n mod 2 (because the initial grid's last cell is n mod 2 and it's never changed).

    # But wait, what if n=1? Then the grid is [1] initially. The target grid must be [1]. But if the target grid is [0] for n=1, then it's impossible.

    # However, the problem states that the initial grid has cell i with i mod 2. So for n=1, the grid is [1]. The target grid must be [1] (if we are to have a valid sequence). But the problem says "Find the number of sequences of operations that result in the integers written in cell i being A_i." So if the target grid does not match the initial grid's first and last cells (and the alternating pattern is broken in a way that the first and last are fixed), then the answer is 0.

    # But wait, the operations can change the grid arbitrarily (within the constraints). However, the first and last cells are never changed. So the target grid must have:
    #   A_1 = 1
    #   A_N = N % 2

    # Now, what about the rest? The grid can be built by merging blocks.

    # Let me define the grid as a sequence of blocks. Each block is a contiguous segment of the same value.

    # The initial grid has blocks of length 1, alternating.

    # Each operation merges two adjacent blocks of the same value (say X) that are separated by