def main():
    data = input().split()
    L = int(data[0])
    R = int(data[1])
    
    if L == 1 and R == 0:
        print("Yes")
    elif L == 0 and R == 1:
        print("Yes")
    else:
        print("Invalid")

if __name__ == "__main__":
    main()