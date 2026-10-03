def main():
    S = input().strip()
    result = ''.join(char for char in S if char == '2')
    print(result)

if __name__ == "__main__":
    main()