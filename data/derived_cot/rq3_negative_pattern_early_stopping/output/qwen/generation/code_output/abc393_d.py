import sys

def main():
    data = sys.stdin.read().splitlines()
    n = int(data[0].strip())
    s = data[1].strip()
    
    # Count the number of ones and record their positions
    ones = []
    for idx, char in enumerate(s):
        if char == '1':
            ones.append(idx)
            
    k = len(ones)
    if k == 0:
        # But guaranteed at least one 1, so this is safe.
        print(0)
        return
        
    # Create the array d: d[j] = ones[j] - j
    d = [ones[j] - j for j in range(k)]
    d.sort()
    
    # The candidate i values: boundaries and medians
    candidates = set()
    candidates.add(0)
    candidates.add(n - k)  # because the block must be of length k, so i <= n-k
    if k % 2 == 1:
        candidates.add(d[k//2])
    else:
        candidates.add(d[k//2 - 1])
        candidates.add(d[k//2])
        
    # We'll consider only candidates in [0, n-k]
    candidates = [i for i in candidates if 0 <= i <= n-k]
    
    # Function to compute cost for a given i
    def cost(i):
        total = 0
        for j in range(k):
            total += abs(d[j] - i)
        return total
        
    ans = float('inf')
    for i in candidates:
        c = cost(i)
        if c < ans:
            ans = c
            
    print(ans)

if __name__ == '__main__':
    main()