import sys

def main():
    data = sys.stdin.read().split()
    it = iter(data)
    n = int(next(it))
    P = [int(next(it)) for _ in range(n)]
    m = int(next(it))
    A = [int(next(it)) for _ in range(m)]
    
    # We'll use a Fenwick Tree (Binary Indexed Tree) to count inversions.
    # But note: we need to update the array and recalc inversion number after each operation.
    # Alternatively, we can use a Wavelet Tree or a Merge Sort Tree, but that might be overkill.
    # Another idea: use a balanced BST and a Fenwick Tree to track the positions and inversion count.
    # But the operations are adjacent swaps, so we can update the inversion count by the change from the swap.
    # However, the operation k is a series of adjacent swaps. We can simulate the operation k by doing the swaps and updating the inversion count for each swap.
    # But the total number of swaps might be too high.

    # Alternatively, we can use a different approach: 
    # Observation: The operations are increasing k, and the sequence A is non-decreasing. 
    # Also, note that once an element is moved beyond a certain position, it won't be affected by smaller k operations.

    # But I recall that the problem is similar to "Bubble Sort Graph" or "Sorting by Adjacent Swaps", and inversion number can be updated by tracking the positions.

    # However, after reading the sample outputs, I see that the inversion number decreases as we apply the operations.

    # Another idea: use a data structure that can handle the following:
    #   - We have an array P.
    #   - We want to perform a bubble pass (operation k) and update the inversion number.
    #   - The inversion number can be updated by the number of inversions created/destroyed by the swaps.

    # But note: the operation k is a bubble pass, which is a sequence of adjacent swaps. Each adjacent swap changes the inversion count by ±1? Actually, no: swapping two adjacent elements changes the inversion count by an odd number (specifically, the change is (number of elements to the left that are greater than the left element and less than the right element) minus (number of elements to the right that are greater than the left element and less than the right element) — wait, no.

    # Actually, the change in inversion count when swapping two adjacent elements (a, b) (at positions i and i+1) is:
    #   Let x = a, y = b.
    #   Before swap: 
    #       Inversions: (i, i+1) if x > y, and for each j < i, if x > P[j] then inversion (j, i), and for each j > i+1, if P[j] < x then inversion (i, j) and if P[j] > y then inversion (i+1, j) — wait, no, the inversion is defined for i < j and P_i > P_j.
    #   After swap: 
    #       Inversions: (i, i+1) if y > x (which is not the case if we swap because x>y), and for each j < i, if y > P[j] then inversion (j, i), and for each j > i+1, if P[j] < y then inversion (i, j) and if P[j] > x then inversion (i+1, j).

    # But this is complicated.

    # Alternatively, we can use a Fenwick Tree to maintain the array and the inversion count. But updating the inversion count after each swap is O(log N), and the total number of swaps might be O(N^2) which is 40e9 for N=200000, which is too slow.

    # We need a better approach.

    # Insight: 
    #   The operations are increasing k, and the sequence A is non-decreasing. 
    #   Also, note that the operations are bubble passes, and the effect of operation k is that the largest element in the first k elements is moved to the k-th position (if we do one pass). 
    #   But actually, one pass moves the largest element to the end of the considered segment (k-th position). 

    #   Moreover, after operation k, the first k elements are such that the largest element is at the end, and the rest are not necessarily sorted.

    #   But if we do operation k multiple times, then the first k elements become sorted.

    #   However, the operations are applied in increasing k, so we are effectively doing bubble sort passes with increasing window sizes.

    #   There is a known fact: the inversion number after bubble sort passes can be computed by considering the