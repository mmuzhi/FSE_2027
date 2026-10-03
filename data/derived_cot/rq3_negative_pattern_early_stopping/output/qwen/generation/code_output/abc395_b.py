def main():
    N = int(input().strip())
    grid = [['.' for _ in range(N)] for _ in range(N)]
    for i in range(1, N+1):
        for j in range(1, N+1):
            # Conditions: i0 <= i, i0 <= j, i0 <= N+1-i, i0 <= N+1-j
            m = min(i, j, N+1-i, N+1-j)
            if m % 2 == 1:
                grid[i-1][j-1] = '#'
            else:
                grid[i-1][j-1] = '.'
    for row in grid:
        print(''.join(row))

if __name__ == '__main__':
    main()