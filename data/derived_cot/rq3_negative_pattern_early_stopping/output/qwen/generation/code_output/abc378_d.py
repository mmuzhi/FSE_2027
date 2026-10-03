from collections import deque

def main():
    import sys
    data = sys.stdin.read().splitlines()
    if not data: 
        print(0)
        return
    H, W, K = map(int, data[0].split())
    grid = []
    for i in range(1, 1+H):
        grid.append(data[i].strip())
    
    # If K is 0, then we are counting the starting cells (each empty cell is a path of 0 moves)
    # But note: the problem says sequences of length K+1, so for K=0, we are counting the starting cells.
    # However, the problem states: "Count the number of ways to start from an empty cell and make K moves"
    # So for K=0, we are just counting the starting cells (each empty cell is a valid path of 0 moves).
    # But note: the problem says "without passing through blocked squares and not visiting the same cell more than once" — for 0 moves, we haven't moved, so we just need to be on an empty cell.

    # But the sample input 2 2 2 has output 2, which is for K=2 (two moves). So we need to consider K moves.

    # We'll do BFS for each starting cell, but we can use DFS with memoization (state: (x, y, visited)) but visited is a set of coordinates.

    # However, K is at most 11, so the maximum depth is 11. The grid is 10x10, so we can do DFS with recursion and memoization.

    # Alternatively, we can use BFS by depth (from 0 to K) and use a state (x, y, visited) but visited is a frozenset.

    # But the state space is too big if we use visited as a frozenset because the grid has 100 cells, but we are only visiting up to 12 cells. The number of states is the number of simple paths of length up to 11, which is the number of ways to choose 12 distinct cells and arrange them, but that's still too many.

    # Alternatively, we can use iterative DFS or BFS without storing the entire visited set, but then we have to avoid cycles. But the problem says no revisiting.

    # Another idea: since K is small (max 11) and the grid is small (10x10), we can use recursion with depth K, and at each step, we mark the visited cells and then unmark. But we need to avoid revisiting the same cell.

    # We can do DFS from each starting cell, and count the number of paths of exactly K moves.

    # Steps:
    # 1. Precompute the grid and the dimensions.
    # 2. For each cell that is empty, start a DFS/BFS that counts the number of paths of length K (K moves, so K+1 cells) without revisiting.
    # 3. We need to avoid blocked cells and revisiting.

    # But doing DFS for each starting cell separately might be inefficient if we do it naively, but K is small (max 11) and the grid is small (10x10). The worst-case number of paths from a starting cell is the number of simple paths of length K, which is bounded by the number of permutations of K+1 distinct cells, but the grid is fixed.

    # However, worst-case, the grid is all empty, and we start at a cell, then we have 4 directions, then 3, then 2, etc. But the branching factor reduces as we visit more cells.

    # Since K is at most 11, the maximum number of steps is 11, so the DFS will go at most 11 deep. The total number of states is the sum over all starting cells of the number of paths of length K from that cell.

    # We can memoize by (x, y, visited) but visited is a frozenset of coordinates. The visited set can be represented by a frozenset of (x, y). The maximum number of visited cells is K+1 (which is 12). The grid has 100 cells, but we are only storing the visited set for each state.

    # The total number of states is the number of simple paths of length up to 11 in the grid. The grid has 100 cells, but we are only visiting 12 at most. The number of states is the number of ways to choose 12 distinct cells and arrange them in a path, but that's still too many.

    # Alternatively, we can use BFS with depth limit K, and use a visited set for each state. But the state space is too big.