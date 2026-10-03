import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1+n]))
    
    even = 0
    odd = -10**18  # a very small number
    
    for i in range(n):
        # Update even and odd states simultaneously using the previous values
        new_even = max(even, odd + 2 * A[i])
        new_odd = max(odd, even + A[i])
        even, odd = new_even, new_odd
        
    print(max(even, odd))

if __name__ == "__main__":
    main()