def main():
    N = input().strip()
    if N.isdigit() and len(N) == 6:
        count1 = N.count('1')
        count2 = N.count('2')
        count3 = N.count('3')
        if count1 == 1 and count2 == 2 and count3 == 3:
            print("Yes")
        else:
            print("No")
    else:
        # According to constraints, N is 6-digit, but just in case input is not 6-digit, we output No.
        print("No")

if __name__ == '__main__':
    main()