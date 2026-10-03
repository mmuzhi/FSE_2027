def main():
    N_str = input().strip()
    a = int(N_str[0])
    b = int(N_str[1])
    c = int(N_str[2])
    first_num = 100 * b + 10 * c + a
    second_num = 100 * c + 10 * a + b
    print(f"{first_num} {second_num}")

if __name__ == '__main__':
    main()