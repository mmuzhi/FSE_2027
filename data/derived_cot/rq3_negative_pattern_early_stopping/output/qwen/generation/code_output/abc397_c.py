import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1+n]))
    
    # Precompute left_distinct array
    left_freq = [0] * (n+1)
    left_arr = [0] * n
    left_distinct = 0
    for i in range(n):
        if left_freq[A[i]] == 0:
            left_distinct += 1
        left_freq[A[i]] += 1
        left_arr[i] = left_distinct
        
    # Precompute right_distinct array
    right_freq = [0] * (n+1)
    right_arr = [0] * n
    right_distinct = 0
    # Traverse from last element to first
    for i in range(n-1, -1, -1):
        if right_freq[A[i]] == 0:
            right_distinct += 1
        right_freq[A[i]] += 1
        right_arr[i] = right_distinct
        
    # Now, find the maximum total for splits from 0 to n-2
    max_val = 0
    for i in range(n-1):
        total = left_arr[i] + right_arr[i+1]
        if total > max_val:
            max_val = total
            
    print(max_val)

if __name__ == "__main__":
    main()