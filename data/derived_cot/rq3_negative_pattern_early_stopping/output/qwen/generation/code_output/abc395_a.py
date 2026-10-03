def main():
    n = int(input().strip())
    data = list(map(int, input().split()))
    for i in range(n - 1):
        if data[i] >= data[i + 1]:
            print("No")
            return
    print("Yes")

if __name__ == '__main__':
    main()