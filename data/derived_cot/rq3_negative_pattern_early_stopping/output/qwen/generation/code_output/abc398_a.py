def main():
    N = int(input().strip())
    if N % 2 == 1:
        # Odd: one '=' in the center
        s = ['-'] * N
        mid = N // 2
        s[mid] = '='
        print(''.join(s))
    else:
        # Even: two adjacent '=' in the center
        s = ['-'] * N
        mid = N // 2
        s[mid] = '='
        s[mid+1] = '='
        print(''.join(s))

if __name__ == '__main__':
    main()