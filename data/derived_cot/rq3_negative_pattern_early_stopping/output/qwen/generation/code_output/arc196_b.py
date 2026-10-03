import sys

MOD = 998244353

def main():
    data = sys.stdin.read().splitlines()
    t = int(data[0])
    index = 1
    results = []
    
    for _ in range(t):
        # Read H and W
        H = int(data[index]); W = int(data[index+1]); index += 2
        grid = []
        for i in range(H):
            grid.append(data[index]); index += 1
            
        # If the grid is empty, then answer is 0? But HW>=2.
        # Precompute the number of A and B tiles.
        # But we need to consider the rotations.
        # We'll use dynamic programming or matrix exponentiation.
        # But the grid is toroidal, so we need to consider cycles.
        # However, the total HW <= 10^6, but the grid is given as H and W.
        # We need to count the number of ways to assign rotations to each tile such that:
        #   For each horizontal edge (cycle): the condition holds.
        #   For each vertical edge (cycle): the condition holds.
        #
        # But note: the condition for an edge is that the two tiles must have the segment.
        # We can precompute for each tile type and each rotation the active edges.
        #
        # Let's define for type A (4 rotations) and type B (2 rotations) the active edges.
        # For type A:
        #   rotation 0: active = {'N', 'E'}
        #   rotation 1: active = {'E', 'S'}
        #   rotation 2: active = {'S', 'W'}
        #   rotation 3: active = {'W', 'N'}
        # For type B:
        #   rotation 0: active = {'N', 'S'}
        #   rotation 1: active = {'E', 'W'}
        #
        # The edges are: 'N', 'E', 'S', 'W'.
        #
        # Now, the condition for a horizontal edge (between tile (i,j) and (i, j+1)) is:
        #   The east edge of (i,j) and the west edge of (i, j+1) must be both active or both not.
        #   But wait, the condition is that both must be active or both not. But the condition is stated as:
        #       "both of the following exist, or neither of the following exists"
        #   So, the east edge of (i,j) and the west edge of (i, j+1) must be both active or both not.
        #   But note: the condition is not "both active" but "both active or both not". So, they must be the same.
        #
        #   Similarly for vertical.
        #
        # Now, we can model the grid as a graph where each node has a set of states (rotations) and each edge has a constraint.
        #
        # But the grid is a torus, so it's a product of two cycles.
        #
        # We can use the following approach:
        #   Let f(i, j) be the rotation of tile (i, j).
        #   Then, the constraints are:
        #       For each (i, j): 
        #           (active('E', f(i, j)) == active('W', f(i, (j+1)%W)))
        #           (active('S', f(i, j)) == active('N', f(i+1, j)))
        #
        #   But note: the condition for the horizontal edge is between (i,j) and (i, (j+1)%W), and for vertical between (i,j) and ((i+1)%H, j).
        #
        #   We can use a DP that goes row by row, but the state space is the product of the rotations of the entire row, which is too big.
        #
        #   Alternatively, we can use the following: the grid is a torus, so we can break the problem into two independent cycles? Not exactly.
        #
        #   Another idea: use the fact that the grid is a torus and the constraints are local to use a matrix of states for a row, and then use the vertical constraints to combine rows.
        #
        #   But the state space for a row is 4^a * 2^b, which is too big.
        #
        #   We need to find a better way.
        #
        #   Let's consider the following: the condition for a horizontal edge is that the east edge of the left tile and the west edge of the right tile are the same (both active or both not). This is a constraint between two adjacent tiles.
        #
        #   We can