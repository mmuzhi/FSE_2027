import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    H = list(map(int, data[1:1+n]))
    
    # We'll compute an array L where L[j] = the index of the nearest building to the left of j (at index j-1 in 0-indexed) that is taller than H[j], or -1 if none.
    # We'll use a stack for the next greater element to the left.
    stack = []
    L_arr = [-1] * n  # For each index j (0-indexed), store the index of the leftmost building taller than H[j] (if exists), else -1.
    for i in range(n):
        # While stack is not empty and the current height is greater than the height at the top of the stack, we pop.
        # But we want the nearest greater to the left, so we pop until we find a greater element.
        while stack and H[stack[-1]] < H[i]:
            stack.pop()
        if stack:
            L_arr[i] = stack[-1]
        else:
            L_arr[i] = -1
        stack.append(i)
    
    # Now, for each i (0-indexed), we want to count the number of j (with j>i) such that the condition holds.
    # But note: the problem asks for each i (from 0 to n-1) the count of j (j>i) satisfying the condition.
    # However, we computed L_arr for each j (0-indexed) as the leftmost building taller than H[j] (if exists). 
    # But note: the condition for a fixed j (0-indexed) is: the segment [i+1, j-1] (in 0-indexed: from i+1 to j-1) must not contain a building taller than H[j].
    # This is equivalent to: i must be greater than L_arr[j] (if L_arr[j] != -1) and i < j.
    # But note: the condition is for a fixed j and varying i (i<j). However, the problem asks for each i, the count of j (j>i) satisfying the condition.

    # We need to reframe: For each i, we want to count the number of j (j>i) such that the condition holds for (i, j).
    # Condition for (i, j): the segment [i+1, j-1] (0-indexed: from i+1 to j-1) does not contain a building taller than H[j].
    # This is equivalent to: the leftmost building taller than H[j] (if exists) must be at an index <= i (so that it is not in [i+1, j-1])? 
    # Actually, no: the condition is that there is no building taller than H[j] in [i+1, j-1]. 
    # We can use the following: For a fixed j, the condition holds for i if and only if i > L_arr[j] (if L_arr[j] != -1) and i < j.
    # But note: if L_arr[j] == -1, then there is no building taller than H[j] to the left of j, so the condition holds for all i from 0 to j-1 (but note: i must be < j).

    # However, we are asked for each i, the count of j (j>i) such that the condition holds.

    # We can do: For each j, the condition holds for i if i > L_arr[j] and i < j.
    # Then, for a fixed j, the valid i are from max(L_arr[j]+1, 0) to j-1 (inclusive). But note: i must be at least 0 and less than j.

    # But note: the problem asks for each i, the count of j (j>i) satisfying the condition.

    # Alternatively, we can fix i and count j. But j>i, and the condition for (i, j) is that the segment [i+1, j-1] does not contain a building taller than H[j].

    # We can use a different approach: 
    #   For each j, we know that the condition holds for i if i > L_arr[j] and i < j.
    #   Then, for each j, we can add 1 to every i in the range [L_arr[j]+1, j-1] (if L_arr[j] != -1) and also for i in the range [0, j-1] if L_arr[j] == -1.

    # But note: the condition is for j>i, so j from i+1 to n-1.

    # We can use a