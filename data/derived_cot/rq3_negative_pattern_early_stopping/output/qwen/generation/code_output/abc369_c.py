import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        print(0)
        return
    n = int(data[0])
    A = list(map(int, data[1:1+n]))
    
    if n == 1:
        print(1)
        return
        
    # Build the diff array (length n-1)
    diff = []
    for i in range(n-1):
        diff.append(A[i+1] - A[i])
        
    # Precompute next_bad: for each index i in [0, n-2], the smallest index j (>=i+1) such that diff[j-1] != diff[i] (if exists) or n (if not found)
    # But note: we want next_bad[i] to be the smallest j (>=i+1) such that the consecutive difference at index j-1 is not equal to diff[i].
    # Actually, we can precompute an array next_bad for indices 0 to n-2.
    # We'll create an array next_bad of length n-1 (for indices 0 to n-2) and initialize with n (meaning not found)
    next_bad = [n] * (n-1)  # n is the next_bad value meaning not found (then we use n as the end index)
    
    # We can do a backward pass or use a dictionary to store the last occurrence of a difference? 
    # Alternatively, we can do a forward pass for each distinct difference? But that would be O(n^2).
    
    # Instead, we can do a simple forward pass for each starting index? But that would be O(n^2).
    
    # We need an efficient way.
    
    # Let's do a backward pass: 
    #   We want for each i (0-indexed in the diff array) the next index j (>=i) such that diff[j] != diff[i].
    #   We can do:
    #       next_occurrence = [n] * (n-1)
    #       last_occurrence = {}
    #       But we want the next occurrence of a different value.
    
    # Alternatively, we can do:
    #   Let next_bad[i] = the smallest j (>=i) in the range [i, n-2] such that diff[j] != diff[i]. Then, the segment starting at index i (in the original array) would have next_bad_original = next_bad[i] + 1 (because the consecutive difference at index j is used for the segment [i, j+1]).
    #   But note: the segment [i, j] (original array) uses consecutive differences from index i to j-1. The condition breaks at the first j (>=i) such that diff[j] != diff[i]. Then, the maximal j in the original array is j+1 (because the segment [i, j+1] would use the consecutive difference at index j, which is bad).
    
    # Actually, we can precompute next_bad for the diff array (which is of length n-1) as follows:
    #   We want for each index i (0-indexed in the diff array) the next index j (>=i) such that diff[j] != diff[i]. 
    #   We can do a backward pass:
    #       Let next_bad_arr = [n-1] * (n-1)   # for the diff array indices, the next_bad_arr[i] will be the next index j (>=i) in [0, n-2] where diff[j] != diff[i]
    #       We can use a dictionary to store the last occurrence of a value? Actually, we want the next occurrence of a different value.
    
    # We can do:
    #   Create an array next_bad_arr of length n-1, initialize with n-1 (the last index of diff is n-2, so n-1 is out of bounds).
    #   Then, we can iterate from right to left and store the next occurrence of a different value.
    
    # Alternatively, we can do:
    #   Let next_bad_arr = [n-1] * (n-1)
    #   We'll create an array to store the next occurrence of the same value? Actually, we want the next occurrence of a different value.
    
    # We can do a simple loop for each i from 0 to n-2:
    #   j = i
    #   while j < n-1 and diff[j] == diff[i]:
    #       j += 1
    #   if j < n-1:
    #       next_bad_arr[i] = j   # j is the first index where the value changes
    #   else:
    #       next_bad_arr[i] = n-1   # meaning no change