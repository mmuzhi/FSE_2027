def main():
    n = int(input().strip())
    a_list = list(map(int, input().split()))
    b_list = list(map(int, input().split()))
    
    max_a = max(a_list)
    max_b = max(b_list)
    
    print(max_a + max_b)

if __name__ == "__main__":
    main()