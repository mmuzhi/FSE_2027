def main():
    import sys
    data = sys.stdin.read().split()
    n = int(data[0])
    c = int(data[1])
    times = list(map(int, data[2:2+n]))
    
    candies = 0
    last_candy_time = -1  # no candy received initially
    
    for t in times:
        if t - last_candy_time >= c:
            candies += 1
            last_candy_time = t
            
    print(candies)

if __name__ == "__main__":
    main()