def main():
    import sys
    data = sys.stdin.read().splitlines()
    n, d = map(int, data[0].split())
    s = data[1].strip()
    m = s.count('@')
    empty_boxes = (n - m) + d
    print(empty_boxes)

if __name__ == "__main__":
    main()