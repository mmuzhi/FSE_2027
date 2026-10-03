def main():
    import sys
    data = sys.stdin.read().split()
    n = int(data[0])
    k = int(data[1])
    A = list(map(int, data[2:2+n]))
    
    part1 = A[n - k:]
    part2 = A[:n - k]
    
    result = part1 + part2
    print(" ".join(map(str, result)))

if __name__ == "__main__":
    main()