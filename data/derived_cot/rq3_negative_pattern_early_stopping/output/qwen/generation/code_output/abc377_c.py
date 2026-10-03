def main():
    import sys
    data = sys.stdin.read().split()
    if not data:
        return
    
    n = int(data[0])
    m = int(data[1])
    pieces = []
    index = 2
    for i in range(m):
        a = int(data[index]); b = int(data[index+1]); index += 2
        pieces.append((a, b))
        
    # The 8 moves from a piece (a, b) to the square (a+dx, b+dy)
    moves = [(2,1), (1,2), (-1,2), (-2,1), (-2,-1), (-1,-2), (1,-2), (2,-1)]
    forbidden = set()
    
    for (a, b) in pieces:
        for dx, dy in moves:
            x = a + dx
            y = b + dy
            if 1 <= x <= n and 1 <= y <= n:
                forbidden.add((x, y))
                
    total_squares = n * n
    answer = total_squares - len(forbidden)
    print(answer)

if __name__ == '__main__':
    main()