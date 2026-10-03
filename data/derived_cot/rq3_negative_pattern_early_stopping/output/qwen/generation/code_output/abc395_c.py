import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1+n]))
    
    # If n is less than 2, then no duplicate possible in a contiguous subarray (since minimal subarray length is 2 for two same numbers)
    if n < 2:
        print(-1)
        return
        
    # Dictionary to store the last occurrence index for each number
    # But we need all occurrences? Actually, we only need the consecutive occurrences to compute the minimal window for each number.
    # We can store the last occurrence and then update as we go, but then we lose the previous occurrences.
    # Alternatively, we can store all indices for each number and then for each number, look at consecutive indices.
    # But note: n can be up to 200000, and numbers up to 10^6, so we can store all indices for each number.

    # We'll create a dictionary: number -> list of indices
    indices = {}
    for i, num in enumerate(A):
        if num not in indices:
            indices[num] = []
        indices[num].append(i)
    
    # Now, for each number, we have a list of indices. We are interested in consecutive pairs in that list.
    min_length = float('inf')
    for num, lst in indices.items():
        # For each consecutive pair in the list of indices for this number
        for j in range(1, len(lst)):
            length = lst[j] - lst[j-1] + 1
            if length < min_length:
                min_length = length
                
    if min_length == float('inf'):
        print(-1)
    else:
        print(min_length)

if __name__ == "__main__":
    main()