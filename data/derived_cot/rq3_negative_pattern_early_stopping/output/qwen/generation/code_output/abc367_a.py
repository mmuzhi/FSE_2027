def main():
    data = input().split()
    A = int(data[0])
    B = int(data[1])
    C = int(data[2])
    
    if B <= C:
        if A < B or A >= C:
            print("Yes")
        else:
            print("No")
    else:  # B > C
        if A < B:
            print("Yes")
        else:
            print("No")

if __name__ == "__main__":
    main()