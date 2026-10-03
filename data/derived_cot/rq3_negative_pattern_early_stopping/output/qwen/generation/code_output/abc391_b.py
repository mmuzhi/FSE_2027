def main():
    import sys
    data = sys.stdin.read().splitlines()
    n, m = map(int, data[0].split())
    s = []
    for i in range(1, 1 + n):
        s.append(data[i].strip())
    t = []
    for i in range(1 + n, 1 + n + m):
        t.append(data[i].strip())
    
    for i in range(n - m + 1):
        for j in range(n - m + 1):
            match = True
            for k in range(m):
                for l in range(m):
                    if s[i + k][j + l] != t[k][l]:
                        match = False
                        break
                if not match:
                    break
            if match:
                print(f"{i + 1} {j + 1}")
                return

if __name__ == "__main__":
    main()