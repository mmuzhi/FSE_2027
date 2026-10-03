def main():
    import sys
    data = sys.stdin.read().splitlines()
    if not data: 
        return
    H, W, D = map(int, data[0].split())
    grid = []
    for i in range(1, 1+H):
        grid.append(data[i].strip())
    
    floor_cells = []
    for i in range(H):
        for j in range(W):
            if grid[i][j] == '.':
                floor_cells.append((i, j))
                
    n = len(floor_cells)
    best = 0
    for i in range(n):
        for j in range(i+1, n):
            a = floor_cells[i]
            b = floor_cells[j]
            count = 0
            for k in range(n):
                x, y = floor_cells[k]
                d1 = abs(x - a[0]) + abs(y - a[1])
                d2 = abs(x - b[0]) + abs(y - b[1])
                if d1 <= D or d2 <= D:
                    count += 1
            if count > best:
                best = count
                
    print(best)

if __name__ == "__main__":
    main()