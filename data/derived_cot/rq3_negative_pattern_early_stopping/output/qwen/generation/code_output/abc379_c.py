import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    m = int(data[1])
    xs = list(map(int, data[2:2+m]))
    as_ = list(map(int, data[2+m:2+2*m]))
    
    total_stones = sum(as_)
    if total_stones != n:
        print(-1)
        return
        
    # We need to check if the leftmost stone is at cell 1 and the distribution is feasible.
    # But wait, the problem is more complex. We need to ensure that we can distribute the stones without creating a deficit in the middle.

    # Let's sort the initial positions and the stone counts.
    sorted_indices = sorted(range(m), key=lambda i: xs[i])
    xs_sorted = [xs[i] for i in sorted_indices]
    as_sorted = [as_[i] for i in sorted_indices]
    
    # Now, we need to check that the cumulative stones from left can cover the cumulative cells from left.
    # We'll traverse from left to right (from cell 1 to cell N) and keep track of the stones available and the deficit.

    # But note: the initial stones are only at specific positions. The rest are zeros.

    # We can think greedily: we need to fill the cells from left to right. We start at cell 1. We must have at least one stone in cell1 or we can move stones to cell1? But wait, we can only move stones to the right, so cell1 must be filled by a stone that is initially at cell1 or we cannot fill it. Actually, no: we can move stones from cell1 to cell2, but we cannot move stones to cell1. So, the only way to have a stone in cell1 is to have an initial stone at cell1. Similarly, for cell2: we can have an initial stone at cell2 or move a stone from cell1 to cell2. But if we don't have an initial stone at cell2, then we must move a stone from cell1 to cell2. But if we move a stone from cell1 to cell2, then cell1 must have at least two stones initially (so that after leaving one in cell1, we have one to move). 

    # Actually, the condition is: at each cell i, the total stones that have been moved to cell i (from the left) plus the initial stones at cell i must be at least the number of stones required to fill cell i (which is 1). But we can also have extra stones that are moved further right.

    # Alternatively, we can use a greedy algorithm:

    # Let's define an array for the entire row? But N can be up to 2e9, so we cannot iterate over all cells.

    # Instead, we can consider the initial positions and the gaps.

    # Steps:

    # 1. Check total stones == N.
    # 2. The leftmost stone must be at cell 1. Otherwise, impossible.
    # 3. Then, we need to check that the cumulative stones from the left can cover the cumulative cells from the left.

    # But wait, the initial stones are at specific positions. We can consider the positions in increasing order.

    # Let's define:
    #   Let events be the initial stones. We'll consider the positions and the stones available.

    # We need to fill the cells from 1 to N. We can only move stones to the right.

    # We can use a greedy method: 
    #   Let current_stones = 0
    #   Let last_position = 0
    #   We'll consider the positions in increasing order.

    # But we have to account for the fact that stones can be moved from a cell to the next, so the stones at a cell can be used to fill the next cell.

    # Actually, we can think of it as: we need to have at least one stone in each cell. The stones can be moved from left to right. So, the condition is that the cumulative stones (including those moved from the left) at each cell must be at least 1.

    # But we can also have extra stones that are moved further right.

    # The idea is to simulate from left to right:

    #   Let current_stones = 0
    #   Let last_position = 0
    #   We'll consider the initial stones in increasing order of position.

    #   For each initial stone at position x with count a:
    #       The distance from last_position to x is d = x - last_position - 1 (the gap between the previous stone and the current one). But wait, we need to fill the cells from last_position+1 to x-1.

    #   Actually, we can consider the entire row as a sequence of cells.