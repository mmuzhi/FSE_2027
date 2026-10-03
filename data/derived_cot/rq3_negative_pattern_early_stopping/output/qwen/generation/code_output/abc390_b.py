def main():
    import sys
    data = sys.stdin.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1+n]))
    
    if n == 2:
        print("Yes")
        return
        
    for i in range(n-2):
        if A[i] * A[i+2] != A[i+1] * A[i+1]:
            print("No")
            return
            
    print("Yes")

if __name__ == "__main__":
    main()