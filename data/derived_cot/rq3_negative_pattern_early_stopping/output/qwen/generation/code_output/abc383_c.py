from collections import deque

def main():
    import sys
    data = sys.stdin.read().splitlines()
    if not data: 
        print(0)
        return
    H, W, D = map(int, data[0].split())
    grid = []
    for i in range(1, 1+H):
        grid.append(data[i].strip())
    
    # If D is 0, then we only consider the cells with 'H' (which are floor cells) and no movement.
    # But note: the problem says "at most D moves", so if D==0, then we can only stay at the humidifier cell.
    # We'll do BFS as described.

    # Initialize distance grid with -1 (unvisited)
    dist = [[-1] * W for _ in range(H)]
    q = deque()
    
    # Directions for neighbors
    directions = [(1,0), (-1,0), (0,1), (0,-1)]
    
    # Start from all 'H' cells
    for i in range(H):
        for j in range(W):
            if grid[i][j] == 'H':
                dist[i][j] = 0
                q.append((i, j))
    
    # BFS
    while q:
        r, c = q.popleft()
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < H and 0 <= nc < W:
                if grid[nr][nc] != '#' and dist[nr][nc] == -1:
                    new_dist = dist[r][c] + 1
                    if new_dist <= D:
                        dist[nr][nc] = new_dist
                        q.append((nr, nc))
    
    # Count the humidified floor cells: floor cells are those that are not '#' and have a non-negative distance (i.e., visited and within D moves)
    count = 0
    for i in range(H):
        for j in range(W):
            if grid[i][j] != '#' and dist[i][j] != -1:
                count += 1
                
    print(count)

if __name__ == "__main__":
    main()