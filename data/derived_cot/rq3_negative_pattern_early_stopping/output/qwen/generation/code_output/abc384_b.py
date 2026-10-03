def main():
    import sys
    data = sys.stdin.read().split()
    n = int(data[0])
    r = int(data[1])
    index = 2
    current_rating = r
    for _ in range(n):
        d = int(data[index])
        a = int(data[index+1])
        index += 2
        if d == 1:
            if 1600 <= current_rating <= 2799:
                current_rating += a
        else:  # d == 2
            if 1200 <= current_rating <= 2399:
                current_rating += a
    print(current_rating)

if __name__ == "__main__":
    main()