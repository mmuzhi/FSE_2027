def main():
    import sys
    data = sys.stdin.read().splitlines()
    n = int(data[0])
    s = data[1].strip()
    
    total_sum = 0
    current = 0
    for i, char in enumerate(s):
        d = int(char)
        # For the first character, we don't have a previous current
        if i == 0:
            current = d
            total_sum += current
        else:
            current = d * (i+1) + 10 * current
            total_sum += current
            
    print(total_sum)

if __name__ == "__main__":
    main()