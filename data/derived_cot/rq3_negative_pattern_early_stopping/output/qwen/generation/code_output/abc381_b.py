def main():
    S = input().strip()
    n = len(S)
    if n % 2 != 0:
        print('No')
        return

    # Check condition 2: for each i, the (2i-1) and 2i characters are equal.
    # Also, condition 3: each character appears exactly two times.

    # First, check condition 2: the string must be composed of pairs.
    for i in range(0, n, 2):
        if S[i] != S[i+1]:
            print('No')
            return

    # Now, check condition 3: each character appears exactly two times.
    from collections import defaultdict
    count = defaultdict(int)
    for char in S:
        count[char] += 1

    # Check that every character that appears has count 2.
    for char in count:
        if count[char] != 2:
            print('No')
            return

    print('Yes')

if __name__ == '__main__':
    main()