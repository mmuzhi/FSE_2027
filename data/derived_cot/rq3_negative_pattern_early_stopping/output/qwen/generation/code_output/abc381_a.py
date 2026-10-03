def main():
    n = int(input().strip())
    s = input().strip()
    if n % 2 == 0:
        print("No")
        return
    mid_index = (n-1)//2
    if s[:mid_index] != '1'*mid_index:
        print("No")
        return
    if s[mid_index] != '/':
        print("No")
        return
    # Check the rest of the string
    if s[mid_index+1:] != '2'*(n - mid_index - 1):
        print("No")
        return
    print("Yes")

if __name__ == '__main__':
    main()