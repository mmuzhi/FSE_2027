def main():
    data = input().split()
    N = int(data[0])
    M = int(data[1])
    
    total = 1
    current = 1
    # If M is 0, then we have only the term for i=0, but M>=1 per constraints, but let's handle M=0 if any.
    # According to constraints, M>=1, but to be safe, we can handle M=0.
    if M == 0:
        print(1)
        return
        
    for i in range(1, M+1):
        current *= N
        total += current
        if total > 10**9:
            print('inf')
            return
            
    print(total)

if __name__ == '__main__':
    main()