def main():
    data = input().split()
    n = int(data[0])
    c1 = data[1]
    c2 = data[2]
    s = input().strip()
    result = []
    for char in s:
        if char == c1:
            result.append(char)
        else:
            result.append(c2)
    print(''.join(result))

if __name__ == "__main__":
    main()