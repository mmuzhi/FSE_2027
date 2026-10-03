from collections import Counter

def main():
    data = list(map(int, input().split()))
    freq = Counter(data)
    total_operations = 0
    for count in freq.values():
        total_operations += count // 2
    print(total_operations)

if __name__ == "__main__":
    main()