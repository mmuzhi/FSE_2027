def main():
    grid = []
    for _ in range(8):
        grid.append(input().strip())
    
    row_has_piece = [False] * 8
    col_has_piece = [False] * 8
    
    for i in range(8):
        for j in range(8):
            if grid[i][j] == '#':
                row_has_piece[i] = True
                col_has_piece[j] = True
                
    count = 0
    for i in range(8):
        for j in range(8):
            if grid[i][j] == '.' and not row_has_piece[i] and not col_has_piece[j]:
                count += 1
                
    print(count)

if __name__ == "__main__":
    main()