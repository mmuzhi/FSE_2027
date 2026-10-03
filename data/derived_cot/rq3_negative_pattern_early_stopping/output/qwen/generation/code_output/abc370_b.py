def main():
    import sys
    data = sys.stdin.read().splitlines()
    N = int(data[0].strip())
    matrix = []
    for i in range(1, N+1):
        row = list(map(int, data[i].split()))
        matrix.append(row)
    
    current = 1
    for k in range(1, N+1):
        if current >= k:
            current = matrix[current-1][k-1]
        else:
            current = matrix[k-1][current-1]
    print(current)

if __name__ == '__main__':
    main()