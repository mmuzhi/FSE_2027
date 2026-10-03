import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    
    it = iter(data)
    H = int(next(it)); W = int(next(it)); N = int(next(it))
    bars = []
    for _ in range(N):
        r = int(next(it)); c = int(next(it)); l = int(next(it))
        bars.append((r, c, l))
    
    # We'll create an array for the final row of each bar, initially set to the initial row.
    # But note: the bars can move multiple times. We need to simulate the falling until no more moves.

    # However, note that the falling is sequential in time steps and the condition is checked at the beginning of each time step.

    # We cannot simulate time steps one by one because 10^100 is too large.

    # Alternative approach: 

    # We note that the grid has H rows and W columns. The bars are given with initial positions.

    # We can use a union-find or a segment tree to keep track of the lowest row that a bar can fall to, but the movement order is by index.

    # Another idea: 

    # We can simulate the falling by processing the bars in increasing index order (from 1 to N) and for each bar, we determine how many steps it can fall.

    # But note: the condition for a bar i is that the cells directly below it (in the current grid state) are free. However, the grid state changes as bars fall.

    # However, because the condition is checked at the beginning of the time step (so the grid state is the one from the previous time step) and the falling of a bar i does not affect the condition for bar i+1 in the same time step, we can think of the falling as happening in discrete "layers" of time steps.

    # Actually, note: the falling of a bar i might be blocked by a bar j (with j>i) that is above it? No, because the condition for bar i is checked at the beginning of the time step (so the grid state is the one from the previous time step) and the bar j (with j>i) has not moved yet (because we process in increasing index). 

    # But wait, the condition for bar i is checked at the beginning of the time step (the grid state from the previous time step) and then bar i moves (if condition holds). Then the next bar (i+1) is processed with the same grid state (from the previous time step) because the condition is checked at the beginning of the time step.

    # This means that the falling of bar i does not affect the condition for bar i+1 in the same time step. 

    # However, the falling of bar i does affect the grid state for the next time step (for the same bar i+1, but in the next time step). 

    # But note: the condition for bar i+1 in the next time step is checked with the grid state from the previous time step (which includes the movement of bar i).

    # Actually, the condition for bar i+1 is checked at the beginning of the time step (which is the state from the previous time step). So the movement of bar i (if it happens) is not reflected in the condition for bar i+1 until the next time step.

    # Therefore, we can simulate the falling of each bar independently, but we must account for the fact that the grid state (the positions of other bars) changes over time.

    # However, note that the falling of a bar i might be blocked by a bar j (with j>i) that is above it? Actually, no: because the condition for bar i is checked at the beginning of the time step (so the grid state is the one from the previous time step) and the bar j (with j>i) has not moved yet (because we process in increasing index) and the bar j is above bar i (so it is not below bar i). 

    # But wait, the condition for bar i is about the cells directly below bar i. The bar j (with j>i) might be above bar i? Then the bar j is not below bar i, so it doesn't block bar i.

    # However, the condition is about the cells directly below bar i. The bar j (with j>i) might be at a row below bar i? Then it would block bar i. But note: the initial state has no overlapping. And the falling order is by index. 

    # Actually, the falling of bar i (with index i) might be blocked by a bar j (with j>i) that is initially below bar i? 

    # Example: 
    #   Bar1: (1,1,1) -> initial row1.
    #   Bar2: (2,1,