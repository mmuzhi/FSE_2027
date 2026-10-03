def main():
    import sys
    data = sys.stdin.read().split()
    n = int(data[0])
    events = []
    index = 1
    for i in range(n):
        t = int(data[index])
        v = int(data[index + 1])
        index += 2
        events.append((t, v))
    
    current_time = 0
    current_water = 0
    
    for t, v in events:
        time_elapsed = t - current_time
        current_water = max(0, current_water - time_elapsed)
        current_water += v
        current_time = t
        
    print(current_water)

if __name__ == '__main__':
    main()