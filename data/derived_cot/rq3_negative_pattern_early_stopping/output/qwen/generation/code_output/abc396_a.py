def main():
    n = int(input().strip())
    arr = list(map(int, input().split()))
    
    for i in range(n - 2):
        if arr[i] == arr[i+1] == arr[i+2]:
            print("Yes")
            return
    print("No")

if __name__ == "__main__":
    main()