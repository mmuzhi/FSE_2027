import bisect

def main():
    import sys
    data = sys.stdin.read().split()
    n = int(data[0])
    arr = list(map(int, data[1:1+n]))
    
    # We are going to count the number of pairs (i, j) with i < j such that arr[i] <= arr[j] / 2.
    # But note: the array is sorted in non-decreasing order.
    # We can use two pointers or binary search.

    # Let's consider: for each j (from 0 to n-1), we want to count the number of i (i < j) such that arr[i] <= arr[j] / 2.
    # However, note: the condition is for the top (which is the smaller one) to be at most half the bottom (the larger one). 
    # But in our sorted array, for a fixed j, the condition is: arr[i] <= arr[j] / 2, and i < j.

    # But note: the same size might appear multiple times, and we want to count distinct pairs (by index) but the condition is on the values.

    # We can do:
    #   Let left = 0
    #   For each j from 0 to n-1, we want to find the largest index i (i < j) such that arr[i] <= arr[j] / 2.
    #   Then the count for j is (i+1) (if we found i) or 0.

    # However, note: the condition is arr[i] <= arr[j] / 2. Since arr is sorted, we can use binary search for the condition.

    # But note: arr[j] / 2 might not be an integer. Since arr[i] are integers, we can use floor division? Actually, the condition is a <= b/2, and a and b are integers. 
    # Example: b=5, then a<=2.5 -> a<=2 (since a is integer). So we can use: condition is arr[i] <= arr[j] // 2 if we use integer division? But note: if arr[j] is odd, then arr[j]//2 is floor division. But the condition is a <= b/2. 
    # For example, b=5, then a<=2.5, so a can be 1 or 2. But if we use floor division, then 5//2=2, so condition is a<=2, which is correct.

    # However, note: the problem says the input values are integers. So we can use integer comparison.

    # But note: the array is sorted, so we can use two pointers.

    # Alternatively, we can precompute the counts for each value and then use a Fenwick tree or segment tree? But n can be up to 500000.

    # Let's use two pointers (one pass with a pointer that moves from left to right).

    # We'll use a two-pointer method:

    # Let left = 0
    # For j from 0 to n-1, we want to find the rightmost index i (i < j) such that arr[i] <= arr[j] / 2.

    # But note: the array is sorted, so we can move a pointer from 0 to n-1 and for each j, we move the left pointer until arr[left] <= arr[j]/2 and arr[left+1] > arr[j]/2? Actually, we want the count of indices i (from 0 to j-1) that satisfy arr[i] <= arr[j]/2.

    # We can do:

    #   j from 0 to n-1:
    #       while left < j and arr[left] <= arr[j] / 2:
    #           left += 1
    #       Then the number of valid i for j is left (because from 0 to left-1 are valid).

    # But wait, that counts the consecutive ones from the beginning. However, the condition is just arr[i] <= arr[j]/2. Since the array is sorted, if arr[i] <= arr[j]/2, then all indices from 0 to i are valid. But note: the condition is independent for each i. However, because the array is sorted, if arr[i] <= arr[j]/2, then arr[i+1] might be <= arr[j]/2 or not. But we want the count of all i from 0 to j-1 that satisfy the condition.

    # Actually, we can use a two-pointer that moves the left pointer only forward. But note: the condition for j might be satisfied by many i's, and then for j+1, the condition might be satisfied by even more i's (since arr[j+1] >= arr[j]).