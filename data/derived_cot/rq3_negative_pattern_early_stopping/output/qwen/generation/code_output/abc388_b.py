def main():
    import sys
    data = sys.stdin.read().split()
    n = int(data[0])
    d = int(data[1])
    snakes = []
    index = 2
    for _ in range(n):
        t = int(data[index])
        l_val = int(data[index + 1])
        index += 2
        snakes.append((t, l_val))
    
    results = []
    for k in range(1, d + 1):
        max_weight = 0
        for t, l_val in snakes:
            new_weight = t * (l_val + k)
            if new_weight > max_weight:
                max_weight = new_weight
        results.append(max_weight)
    
    for res in results:
        print(res)

if __name__ == "__main__":
    main()