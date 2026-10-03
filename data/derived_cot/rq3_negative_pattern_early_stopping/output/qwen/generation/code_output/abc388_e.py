import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    arr = list(map(int, data[1:1+n]))
    
    # We are going to use a greedy matching from the largest to the smallest.
    # We want to form as many pairs as possible. We can use a two-pointer or binary search.

    # Let's consider: we want to assign a top for each bottom. The condition is: top <= bottom/2.
    # We can try to use the smallest available top for a bottom? Actually, we want to save the larger tops for the larger bottoms? Not exactly.

    # Alternatively, we can use a greedy matching from the largest bottom and match it with the largest top that is <= bottom/2, but that might not maximize the count.

    # Actually, we can use a two-pointer from the end (largest) and from the beginning (smallest) but that doesn't work because the condition is not symmetric.

    # Another idea: we can use a greedy matching by considering the condition: for a bottom, we need a top that is at most half. We can use a two-pointer from the end (bottom) and from the beginning (top) but we have to be careful.

    # Let's try: 
    #   We want to form pairs. We can use a two-pointer that starts from the largest and the smallest, but we need to assign a top for a bottom.

    # Actually, we can use a greedy matching from the largest to the smallest, and for each bottom, we try to find the smallest top that satisfies 2 * top <= bottom. But that might not be efficient.

    # Alternatively, we can use a greedy matching by iterating from the largest to the smallest and use a pointer for the tops.

    # We can do: 
    #   Sort the array (already sorted).
    #   Then, we can use a two-pointer for the tops and bottoms, but we need to assign each bottom a top.

    # Another idea: use a greedy matching by considering that the condition is 2 * top <= bottom. We can try to match the smallest available top that is <= bottom/2. But we want to maximize the number of pairs, so we should use the smallest top for the smallest bottom? 

    # Actually, we can use a greedy matching from the largest to the smallest for the bottoms and use a pointer for the tops that are available.

    # Steps:
    #   Let's have two pointers, one for the bottom (starting from the largest) and one for the top (starting from the smallest).
    #   But note: the condition is 2 * top <= bottom. We want to assign a top to a bottom. We can try to assign the smallest top that satisfies the condition for the largest bottom? Actually, we want to use the smallest top that is available and satisfies the condition, so that we leave larger tops for larger bottoms (which require larger tops? Actually, no: the condition for a larger bottom is easier to satisfy because the top can be larger, but we are constrained by the available tops.

    # Actually, we can use a two-pointer from the beginning and the end, but we need to assign tops to bottoms. We can do:

    #   Let left = 0, right = n-1.
    #   We want to count the number of pairs.

    #   But note: the condition is 2 * top <= bottom. We can try to match the smallest top that is <= bottom/2. However, we can also use a greedy matching by iterating from the largest to the smallest for the bottom and then for each bottom, we find the largest top that is <= bottom/2, but that might not be efficient.

    # Alternatively, we can use a greedy matching by iterating from the smallest to the largest and try to assign a bottom for a top? But the condition is defined with the top being the smaller one.

    # Actually, we can use a two-pointer that starts from the smallest and the largest, but we need to assign a bottom and a top.

    # Let me think: We want to form pairs (top, bottom) such that 2 * top <= bottom. We can use a greedy matching from the largest bottom and match it with the largest top that is <= bottom/2, but then we remove both and continue. However, that might not be optimal.

    # Actually, we can use a greedy matching from the largest to the smallest for the bottom and for each bottom, we find the smallest top that is <= bottom/2 (to save larger tops for larger bottoms). But note: we are allowed to choose any 2K, so we want to maximize the count.

    # We can do:

    #   Sort the array (already sorted).
    #   Let's use two pointers: one for the bottom (starting from the largest) and one for the