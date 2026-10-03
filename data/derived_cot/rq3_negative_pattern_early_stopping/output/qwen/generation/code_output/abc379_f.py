import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    q = int(data[1])
    H = list(map(int, data[2:2+n]))
    queries = []
    index = 2+n
    for i in range(q):
        l = int(data[index]); r = int(data[index+1]); index += 2
        queries.append((l, r))
    
    # Precompute the nearest greater or equal to the left for each index.
    # We'll create an array "prev_idx" of length n+1 (1-indexed) such that prev_idx[i] is the index of the nearest building to the left (at position j < i) with height >= H[i-1] (if exists), or 0 if none.
    # We'll use a stack to compute the previous greater or equal element.
    prev_idx = [0] * (n+1)  # 1-indexed, prev_idx[i] for building i (0-indexed position i-1)
    stack = []
    # We'll process from left to right.
    # We are going to compute for each building i (0-indexed) the previous greater or equal element.
    # We'll store (height, index) in the stack.
    # But note: our array H is 0-indexed, so building i is at index i (0-indexed) and has height H[i].
    # We want for building i (0-indexed) the nearest j (0-indexed) to the left such that H[j] >= H[i].
    # Then, we'll store the index (j+1) for 1-indexed? Actually, we can store 0-indexed indices and then adjust.
    # Let's do 0-indexed for the stack.

    # We'll create an array "prev" for 0-indexed indices.
    prev = [-1] * n  # for 0-indexed, prev[i] = the index j (0-indexed) of the previous greater or equal element, or -1 if none.
    stack = []
    for i in range(n):
        # Pop until the top of the stack is greater than or equal to H[i] (or stack empty)
        while stack and H[stack[-1]] < H[i]:
            stack.pop()
        if stack:
            prev[i] = stack[-1]
        else:
            prev[i] = -1
        stack.append(i)

    # Now, for each building i (0-indexed), the nearest building to the left (in the entire array) that is >= H[i] is at index prev[i] (0-indexed). 
    # But note: the condition for a building k (0-indexed index i) to be visible from both l and r (1-indexed) is that the nearest building to the left (>=H[i]) must be at an index < l (1-indexed). 
    # But note: our prev[i] is 0-indexed. The condition in 1-indexed: the nearest building to the left (>=H[i]) is at position (prev[i]+1) (1-indexed). We require that (prev[i]+1) < l (1-indexed). 
    # But wait, the query gives l and r in 1-indexed. The building k is at 0-indexed index i, then its 1-indexed index is i+1. The condition is that the nearest building to the left (>=H[i]) is at 1-indexed index (prev[i]+1) and we require that (prev[i]+1) < l (1-indexed). 

    # However, note: the condition is that the nearest building to the left (>=H[i]) must be at an index < l (1-indexed). But the building k is at index i (0-indexed) and we are considering the entire array. The nearest building to the left (>=H[i]) is at index prev[i] (0-indexed). The 1-indexed index of that building is prev[i]+1. We require that prev[i]+1 < l (1-indexed). 

    # But note: the query asks for buildings to the east of building r (1-indexed). So k (0-indexed) must be at index >= r (1-indexed) -> k (0-indexed) >= r (1-indexed) - 1? Actually, the building r is at 0-indexed index r-1. The buildings to the east are from index r (0-indexed) to n-1.

    # So, for a building k (0-indexed index i, with i from r to n-1, where r is the 0-indexed index = r-1) we need to check that the nearest building to the left (