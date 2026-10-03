import sys

def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    index = 1
    results = []
    for _ in range(t):
        R = int(data[index]); B = int(data[index+1]); index += 2
        total = R + B
        # Conditions for impossibility:
        # 1. If there are no pieces, but total>=2 so not applicable.
        # 2. The cycle must be closed. The moves must form a cycle.
        # Observing small cases and known examples:
        # Sample: 
        #   "2 3" -> Yes
        #   "1 1" -> No
        #   "4 0" -> Yes (all red)
        # 
        # Let's analyze:
        # - If all pieces are red (B=0), then we need a cycle of red moves (horizontal/vertical). 
        #   This is possible if the cycle is a closed loop (like a rectangle). But note: the cycle must be of length total (R+B) and each consecutive move is horizontal/vertical. 
        #   However, the problem is that the board is huge, so we can form a cycle arbitrarily. But note: the cycle must have distinct squares. 
        #   Actually, for all red, we can form a cycle if total >= 2. For example, for two reds: we can place them at (1,1) and (1,2). Then from (1,1) to (1,2) is horizontal, and from (1,2) to (1,1) is horizontal? But wait, the last piece must move to the first. So, the cycle is two nodes: node1 and node2. Then node1 (red) must move to node2 (red) and node2 (red) must move to node1 (red). 
        #   For two reds: 
        #       Place red1 at (1,1), red2 at (1,2). Then from red1 (1,1) to red2 (1,2) is horizontal (allowed). From red2 (1,2) to red1 (1,1) is horizontal (allowed). So, two reds is possible.
        #   Similarly, three reds: we can form a triangle? But red moves are horizontal/vertical, so we can only move to adjacent squares. So, a cycle of three reds: 
        #       (1,1) -> (1,2) -> (2,2) -> (1,1). 
        #       (1,1) to (1,2): horizontal
        #       (1,2) to (2,2): vertical
        #       (2,2) to (1,1): diagonal? But wait, (2,2) to (1,1) is diagonal, but the piece at (2,2) is red, so it can only move horizontally/vertically. So, from (2,2) to (1,1) is not allowed for red. 
        #   So, three reds: we need a cycle of three reds with each consecutive move being horizontal/vertical. But in a grid, the smallest cycle for horizontal/vertical moves is 4 (a square). So, three reds is impossible? 
        #   Actually, no: we can form a cycle of three reds if we use a different shape? But in a grid, three distinct squares with each consecutive move being horizontal/vertical and the last connecting back to the first? 
        #   Example: 
        #       (1,1) -> (1,2) -> (2,2) -> (2,1) -> (1,1) is a cycle of four. But we need three. 
        #   For three: 
        #       (1,1) -> (1,2) -> (2,2) -> (1,1) is not allowed because (2,2) to (1,1) is diagonal (not allowed for red). 
        #   Alternatively, (1,1) -> (1,2) -> (1,3) -> (1,1) is not allowed because (1,3) to (1,1) is two steps (not adjacent). 
        #   So, three reds is impossible. 
        #   Similarly, four reds is possible (a square). 
        #   So, for all red, the cycle must be of even length? Actually, no: the grid graph is bipartite (like a chessboard). The red pieces are moving on a grid, and the grid is bipartite (black and white squares). Each move changes the color (if we color the grid in chessboard fashion). So,