def main():
    data = input().split()
    A = int(data[0])
    B = int(data[1])
    C = int(data[2])
    total = A + B + C
    if total % 2 != 0:
        print("No")
    else:
        half = total // 2
        if A == half or B == half or C == half:
            print("Yes")
        else:
            # Check if any two numbers sum to half
            if A + B == half or A + C == half or B + C == half:
                print("Yes")
            else:
                print("No")

if __name__ == "__main__":
    main()