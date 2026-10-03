import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1+n]))
    
    max_val = 100000
    # Precompute divisors for all numbers up to max_val
    divisors = [[] for _ in range(max_val+1)]
    for i in range(1, max_val+1):
        for j in range(i, max_val+1, i):
            divisors[j].append(i)
    
    # Precompute Grundy numbers for all numbers from 1 to max_val
    g = [0] * (max_val+1)
    # g[1] is 0, as base case.
    # We'll compute from 2 to max_val
    for num in range(2, max_val+1):
        s = set()
        for d in divisors[num]:
            if d < num:
                s.add(g[d])
        mex_val = 0
        while mex_val in s:
            mex_val += 1
        g[num] = mex_val

    # Now, compute the XOR of the Grundy numbers for the input list A
    total = 0
    for a in A:
        total ^= g[a]
    
    if total != 0:
        print("Anna")
    else:
        print("Bruno")

if __name__ == "__main__":
    main()