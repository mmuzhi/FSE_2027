def main():
    data = input().split()
    A = int(data[0])
    B = int(data[1])
    s = set()
    s.add(2*A - B)
    s.add(2*B - A)
    if (A+B) % 2 == 0:
        s.add((A+B)//2)
    print(len(s))

if __name__ == '__main__':
    main()