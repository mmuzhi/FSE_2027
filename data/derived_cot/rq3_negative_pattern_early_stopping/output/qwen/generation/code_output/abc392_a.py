def main():
    data = input().split()
    a = int(data[0])
    b = int(data[1])
    c = int(data[2])
    
    if a * b == c or a * c == b or b * c == a:
        print("Yes")
    else:
        print("No")

if __name__ == "__main__":
    main()