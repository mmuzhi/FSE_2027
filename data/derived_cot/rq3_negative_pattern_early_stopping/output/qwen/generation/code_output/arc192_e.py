import sys
from math import comb as _comb

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    W = int(data[0]); H = int(data[1]); L = int(data[2]); R = int(data[3]); D = int(data[4]); U = int(data[5])
    
    # Total number of allowed points is not needed, but we can compute the answer by considering the grid as four parts.

    # However, the problem is complex and requires advanced combinatorial mathematics.

    # After careful thought, we can use the following approach:

    # The grid is divided into four regions by the forbidden rectangle [L, R] x [D, U].

    # We can consider the grid as having four corners:

    # 1. Bottom-left: x in [0, L-1], y in [0, D-1]
    # 2. Bottom-right: x in [R+1, W], y in [0, D-1]
    # 3. Top-left: x in [0, L-1], y in [U+1, H]
    # 4. Top-right: x in [R+1, W], y in [U+1, H]

    # And the middle parts (the strips) are also allowed.

    # But note: the bottom strip (y < D) is allowed for all x, and the top strip (y > U) is allowed for all x, and the left strip (x < L) for all y, and the right strip (x > R) for all y.

    # The key is to use the fact that the grid is a directed acyclic graph (DAG) with edges only to the right and up.

    # We can use dynamic programming with state (x, y) but only at the boundaries of the forbidden area.

    # However, the grid is too large.

    # Alternative approach: use the inclusion-exclusion principle to count the total number of paths that start in the allowed area and end in the allowed area, avoiding the forbidden area.

    # But the forbidden area is a rectangle, and the grid is huge.

    # Another idea: use the concept of "free paths" and "blocked paths".

    # We can compute the total number of paths if there were no forbidden area, and then subtract the paths that go through the forbidden area.

    # But the total number of paths without forbidden area is the sum over all starting points (a, b) of the number of paths from (a, b) to all (c, d) with c >= a, d >= b. This is too large.

    # We need a better approach.

    # After research, I recall that for grid paths with a forbidden rectangle, we can use the following:

    # Let F(x, y) be the number of paths from (x, y) to the boundary of the forbidden area (or to the end of the grid) without entering the forbidden area.

    # But then we have to sum over all starting points.

    # But the grid is huge.

    # Another idea: use the principle of "reflection" or "complementary counting" but for a rectangle.

    # However, after careful thought, I found that the problem can be broken down into four independent parts:

    # 1. The bottom-left part: x from 0 to L-1, y from 0 to D-1.
    # 2. The bottom-right part: x from R+1 to W, y from 0 to D-1.
    # 3. The top-left part: x from 0 to L-1, y from U+1 to H.
    # 4. The top-right part: x from R+1 to W, y from U+1 to H.

    # And then the middle parts (the strips) are also allowed, but the strips are connected to the corners.

    # But note: the bottom strip (y < D) is allowed for all x, so we can also have paths that start in the bottom strip (x from L to R) and then move right or up.

    # This is getting too complex.

    # Given the complexity and the constraints, I decide to use the following method:

    # We can use dynamic programming with state (x, y) but only for x in {0, L, R, W} and y in {0, D, U, H}. But then how to account for the entire grid?

    # Actually, we can use the following combinatorial formula for the number of paths from (a, b) to (c, d) that avoid the forbidden rectangle [L, R] x [D, U]:

    # The number of paths from (a, b) to (c, d) that avoid the forbidden