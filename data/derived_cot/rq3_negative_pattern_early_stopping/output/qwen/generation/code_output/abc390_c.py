def main():
    import sys
    data = sys.stdin.read().splitlines()
    if not data: 
        print("No")
        return
    H, W = map(int, data[0].split())
    grid = []
    for i in range(1, H+1):
        grid.append(data[i].strip())
    
    # If there is only one cell and it is black, then it's a 1x1 rectangle -> Yes.
    # But note: the grid might have multiple rows and columns.

    # Step 1: Collect all fixed black and fixed white positions.
    fixed_black = []  # (i, j)
    fixed_white = []  # (i, j)

    for i in range(H):
        for j in range(W):
            if grid[i][j] == '#':
                fixed_black.append((i, j))
            elif grid[i][j] == '.':
                fixed_white.append((i, j))

    # If there are no fixed black, then we cannot form a rectangle (since there must be at least one black by the problem statement, but the constraint says there is at least one black, so we don't need to handle this).
    # However, the constraint says "There is at least one cell that is already painted black", so fixed_black is non-empty.

    # Step 2: Find the minimal bounding box of fixed_black.
    if fixed_black:
        rows = [i for i, j in fixed_black]
        cols = [j for i, j in fixed_black]
        min_row, max_row = min(rows), max(rows)
        min_col, max_col = min(cols), max(cols)
    else:
        # According to the constraint, there is at least one black, so this should not happen.
        print("No")
        return

    # The rectangle must at least cover [min_row, max_row] x [min_col, max_col]. But we can extend it.

    # However, we must ensure that the entire rectangle does not contain any fixed white.

    # But note: the rectangle must be contiguous and the entire grid must be partitioned: the rectangle is black, the rest is white.

    # The rectangle must be chosen such that:
    #   a <= min_row, b >= max_row, c <= min_col, d >= max_col.
    #   And the rectangle must not include any fixed white.

    # But note: we are allowed to extend arbitrarily? Actually, we can extend to the entire grid? But then we must check that the entire grid doesn't have fixed white? Actually, no: the rectangle must not include fixed white, so we cannot extend to a row or column that has a fixed white.

    # However, we can choose the rectangle arbitrarily as long as it covers the fixed black and avoids fixed white.

    # Let's define the candidate rectangle: the minimal one is [min_row, max_row] x [min_col, max_col]. But we can also consider extending the rectangle to the left, right, top, bottom if there are no fixed white in the extended areas.

    # But note: we can also choose a rectangle that is larger than the minimal bounding box, but we must avoid fixed white.

    # However, the problem does not require the rectangle to be minimal. So we can choose the rectangle to be the minimal bounding box if it doesn't contain fixed white, or we can choose a larger one (if the extended areas don't contain fixed white) but note: the fixed white might be outside the minimal bounding box, so we must avoid them.

    # Actually, the rectangle must not include any fixed white. So the rectangle must be contained in the complement of fixed_white.

    # But note: the fixed_white are fixed and cannot be changed. So the rectangle must not cover any fixed_white.

    # Now, the minimal bounding box might include a fixed_white? Then we cannot use the minimal bounding box. But we can extend the rectangle to avoid the fixed_white? Actually, no: if the minimal bounding box includes a fixed_white, then we cannot use the minimal bounding box because we cannot change the fixed_white to white (it's already white) and we cannot change the fixed_white to black (because then the rectangle would include a white cell, which is not allowed). So the minimal bounding box must not include any fixed_white.

    # However, what if the fixed_white is inside the minimal bounding box? Then the minimal bounding box is invalid. But note: the fixed_white is already white, so if the minimal bounding box includes a fixed_white, then that fixed_white is inside the rectangle, which is not allowed.

    # Therefore, the minimal bounding box must not contain any fixed_white.

    # But wait: the minimal bounding box is defined by the fixed_black. The fixed_white might be inside the bounding box? Then we cannot use the minimal bounding box.

    # Actually, the rectangle must cover all fixed_black