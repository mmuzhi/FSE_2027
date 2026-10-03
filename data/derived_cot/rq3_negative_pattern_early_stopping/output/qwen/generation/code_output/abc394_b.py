def main():
    n = int(input().strip())
    strings = [input().strip() for _ in range(n)]
    sorted_strings = sorted(strings, key=lambda x: len(x))
    result = ''.join(sorted_strings)
    print(result)

if __name__ == "__main__":
    main()