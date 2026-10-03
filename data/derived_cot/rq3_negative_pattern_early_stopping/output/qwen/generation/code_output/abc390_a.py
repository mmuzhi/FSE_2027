def is_sorted(arr):
    for i in range(4):
        if arr[i] > arr[i+1]:
            return False
    return True

def main():
    data = list(map(int, input().split()))
    if is_sorted(data):
        print("No")
        return

    # Check all adjacent swaps
    n = len(data)
    for i in range(n-1):
        # Create a copy of the array
        temp = data.copy()
        # Swap adjacent elements at i and i+1
        temp[i], temp[i+1] = temp[i+1], temp[i]
        if is_sorted(temp):
            print("Yes")
            return

    print("No")

if __name__ == "__main__":
    main()