import itertools

def main():
    import sys
    data = sys.stdin.read().split()
    n = int(data[0])
    k = int(data[1])
    R = list(map(int, data[2:2+n]))
    
    ranges = [range(1, r+1) for r in R]
    sequences = itertools.product(*ranges)
    
    for seq in sequences:
        if sum(seq) % k == 0:
            print(" ".join(map(str, seq)))

if __name__ == '__main__':
    main()