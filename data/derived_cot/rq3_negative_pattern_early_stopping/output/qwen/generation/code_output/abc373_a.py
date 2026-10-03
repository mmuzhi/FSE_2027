def main():
    strings = []
    for _ in range(12):
        strings.append(input().strip())
    
    count = 0
    for i in range(12):
        if len(strings[i]) == i + 1:
            count += 1
            
    print(count)

if __name__ == "__main__":
    main()