import heapq

def main():
    import sys
    data = sys.stdin.read().split()
    it = iter(data)
    H = int(next(it)); W = int(next(it)); X = int(next(it))
    P = int(next(it)); Q = int(next(it))
    grid = []
    for _ in range(H):
        row = [int(next(it)) for _ in range(W)]
        grid.append(row)
    
    # Directions for adjacent cells
    dirs = [(1,0), (-1,0), (0,1), (0,-1)]
    
    # dp[i][j] = minimal total strength (initial + absorbed) to be adjacent to (i, j)
    dp = [[10**18] * W for _ in range(H)]
    # We start at (P-1, Q-1) with strength grid[P-1][Q-1]
    start_i = P-1
    start_j = Q-1
    dp[start_i][start_j] = grid[start_i][start_j]
    
    # Priority queue: (total_strength, i, j)
    heap = [(grid[start_i][start_j], start_i, start_j)]
    
    while heap:
        total, i, j = heapq.heappop(heap)
        if total != dp[i][j]:
            continue
        # Check if we can absorb adjacent cells from (i, j)
        for dx, dy in dirs:
            ni, nj = i + dx, j + dy
            if 0 <= ni < H and 0 <= nj < W:
                # Condition to absorb (ni, nj): total (current total strength) must be > X * grid[ni][nj]
                if total > X * grid[ni][nj]:
                    new_total = total + grid[ni][nj]
                    if new_total < dp[ni][nj]:
                        dp[ni][nj] = new_total
                        heapq.heappush(heap, (new_total, ni, nj))
    
    # The answer is the maximum total strength we can achieve? 
    # But note: we are storing the minimal total strength to be adjacent to each cell. 
    # However, we can absorb a cell only once, and the total strength is the sum of the initial and all absorbed.
    # But note: the problem asks for the maximum possible strength of Takahashi.
    # We can also not absorb all cells. We need to consider the entire connected component? 
    # Actually, we can only absorb cells that are connected to the start. And we want the maximum total strength (initial + absorbed) that we can achieve.
    # But note: the condition for absorbing a cell is checked at the moment of absorption, and we can choose the order arbitrarily (as long as the condition holds). 
    # However, the Dijkstra we did is for the minimal total strength to be adjacent to a cell. But note: the condition for absorbing a cell is that the total strength (at the moment) is > X * S[cell]. 
    # We can also consider: the maximum total strength is the sum of the initial and all cells that we can absorb (if we can absorb them in an order that satisfies the condition). 
    # But note: the condition must hold at the moment of absorption. 
    # However, the problem does not require us to absorb all cells. We can stop at any time. 
    # But note: the condition for absorbing a cell is independent of the order of absorption for the same cell (if we can absorb it, then we can absorb it at the moment we are adjacent). 
    # Actually, the total strength is the sum of the initial and all absorbed cells. And we can absorb a cell only if the condition holds at the moment of absorption. 
    # But note: the condition for a cell (i,j) is: total_strength (at the moment) > X * S[i][j]. 
    # The total_strength at the moment is the sum of the initial and all absorbed cells (including the ones that are part of the path to (i,j)). 
    # However, the Dijkstra we did is for the minimal total strength to be adjacent to (i,j). But note: the condition for absorbing (i,j) is that the total_strength (which is the sum of the initial and all absorbed) must be > X * S[i][j]. 
    # But note: the minimal total_strength to be adjacent to (i,j) might not be the one that satisfies the condition for absorbing (i,j). 
    # Actually, we can use the following: 
    #   We want to compute the maximum total strength (initial + absorbed) that we can achieve. 
    #   But note: the condition for absorbing a cell (i,j) is that the total_strength (at the moment) must be > X * S[i][j].