import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    xs = list(map(int, data[1:1+n]))
    
    # We are allowed to perform operations that can be thought of as reflecting inner pieces over the midpoint of two outer pieces.
    # The key observation is that the operations can be used to "transfer" the positions in a way that the minimal sum is achieved when the pieces are as left as possible, but the operations are constrained by the outer pieces.
    # However, note that the operations can be performed repeatedly and the problem can be transformed into a problem of "freezing" the outermost pieces and then moving the inner ones.

    # Actually, note that the operation does not change the set of "outer" pieces. The outermost pieces (the smallest and largest) cannot be moved because they are never used as the inner pieces (since the operation requires an i such that i+3 exists, so the inner pieces are at least the second and third). 

    # But wait, in the operation, the outer pieces (i-th and i+3-th) are used to define the midpoint. So the outermost pieces (the very first and the very last) are never moved because they are never the inner pieces. 

    # Therefore, the minimal sum must have the outermost pieces fixed at their original positions. 

    # Then, the problem reduces to: we can move the inner pieces arbitrarily (by a series of reflections) as long as the order is preserved and the outermost pieces are fixed.

    # But note: the operations can be performed repeatedly. 

    # Another observation: the operation is linear and can be seen as a transformation that can be applied independently on overlapping intervals. 

    # However, there is a known approach for such problems: the minimal sum is achieved when the pieces are as left as possible, but the leftmost and rightmost are fixed. 

    # Actually, the problem is similar to the "minimum sum of absolute values" or "minimum sum of coordinates" with reflection operations.

    # Let me consider the effect on the entire array. 

    # We can think of the operations as allowing us to "fold" the array from the ends. 

    # But note: the operation is defined on four consecutive pieces. 

    # Alternatively, we can consider that the operations allow us to "simulate" a process where we can move the inner pieces to the left or right, but the goal is to minimize the sum, so we want to move them left.

    # However, the operation can also move pieces to the right if the midpoint is to the right of the current positions. 

    # But the goal is to minimize the sum, so we want to move the pieces as left as possible.

    # But the operations are constrained by the outer pieces. 

    # Another idea: the minimal sum is independent of the order of operations and only depends on the initial and final positions. 

    # We can model the problem as: we have a set of points, and we can perform operations that reflect two adjacent points over the midpoint of two other points (with the two outer points fixed). 

    # But note: the operation is defined on four consecutive points (in sorted order). 

    # Since the array is sorted initially and the operations preserve the order, we can consider the array as fixed in order.

    # Let me denote the array as a[0], a[1], ..., a[n-1].

    # The operation on i (0-indexed, i from 0 to n-4) will change a[i+1] and a[i+2] to:
    #   a[i+1] = a[i] + a[i+3] - a[i+1]
    #   a[i+2] = a[i] + a[i+3] - a[i+2]

    # But wait, that's the same as the formula above.

    # Now, note that we can perform operations repeatedly. 

    # The key is to notice that the operations can be performed in any order, and the minimal sum is achieved when we have "folded" the array as much as possible from the ends.

    # Actually, the problem is equivalent to: we can choose to "fix" some of the inner pieces by reflecting them over the outer ones, and the minimal sum is the sum of the outermost pieces plus the minimal possible positions for the inner ones.

    # But how to compute that?

    # Let me consider the following: 

    # The operations allow us to "transfer" the positions of the inner pieces. 

    # Actually, there is a known solution for a similar problem: the minimal sum is the sum of the first and last piece, and then for the inner pieces, we can choose to either keep them or reflect them. But wait, the operations are constrained.

    # Alternatively, we can use dynamic programming