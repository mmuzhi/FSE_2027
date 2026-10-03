import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1+n]))
    
    # We'll create an array B of -1's (to be filled with 1-indexed positions or -1)
    B = [-1] * n
    last_occurrence = {}  # maps number to the last 0-indexed index where it was found
    
    for i in range(n):
        num = A[i]
        if num in last_occurrence:
            # The last_occurrence[num] is the 0-indexed index of the previous occurrence
            # We set B[i] to last_occurrence[num] + 1 (to convert to 1-indexed)
            B[i] = last_occurrence[num] + 1
        else:
            B[i] = -1
            
        # Update the last_occurrence for num to the current index (0-indexed)
        last_occurrence[num] = i
        
    # Now, we output the B array as space separated values
    print(" ".join(map(str, B)))

if __name__ == "__main__":
    main()