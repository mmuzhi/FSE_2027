import sys

def main():
    q = int(sys.stdin.readline())
    counts = {}
    distinct = set()
    for _ in range(q):
        data_line = sys.stdin.readline().split()
        if not data_line:
            continue
        t = int(data_line[0])
        if t == 1:
            x = int(data_line[1])
            counts[x] = counts.get(x, 0) + 1
            if counts[x] == 1:
                distinct.add(x)
        elif t == 2:
            x = int(data_line[1])
            counts[x] = counts.get(x, 0) - 1
            if counts[x] == 0:
                distinct.remove(x)
        else:
            print(len(distinct))

if __name__ == '__main__':
    main()