import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    m = int(data[1])
    A = list(map(int, data[2:2+n]))
    
    # We'll precompute the inversion count for the entire array A (for k=0, but actually k=0 is when all are in Set1)
    # But note: for k=0, Set1 is all elements (since A_i < M, and k=0, so A_i < M-0 = M, which is true). So inversion count for k=0 is the inversion count of A.
    # However, we need to compute inversion counts for each k.

    # Let's define:
    #   Set1: indices i such that A_i < m - k
    #   Set2: indices i such that A_i >= m - k

    # The inversion count for a fixed k is:
    #   inversion_count(Set1) + inversion_count(Set2)

    # But note: the inversion condition is the same as in A for the pairs in the same set.

    # However, we cannot iterate over each k and then over each element (O(n) per k) because M and n can be up to 200,000.

    # We need to find a way to compute the inversion counts for Set1 and Set2 for each k quickly.

    # Let's reframe:

    # Consider that k goes from 0 to m-1. Then the threshold is t = m - k (for Set1: A_i < t, Set2: A_i >= t).

    # As k increases, t decreases (from m to 1).

    # We can think of t as a parameter from m down to 1.

    # We need to compute for each t (from m down to 1) the inversion count of the elements < t and the inversion count of the elements >= t.

    # But note: the inversion count for the entire array A is fixed. However, the inversion count for Set1 and Set2 are not independent.

    # Alternatively, we can use a Fenwick Tree or Segment Tree to compute inversion counts for subsequences.

    # But note: the inversion count for a subsequence (Set1) is the number of pairs (i, j) (with i < j) such that A_i > A_j and A_i, A_j in Set1.

    # We can use a Fenwick Tree to count inversions, but we need to do it for each t (each k) and t goes from m down to 1.

    # Steps:

    # 1. Precompute the inversion count for the entire array (for k=0) but that's not directly helpful.

    # 2. We can use a two-pointer approach or a sweep line.

    # Let me consider: 

    #   Let F(t) = inversion count for elements < t (Set1) and G(t) = inversion count for elements >= t (Set2).

    #   Then answer for k = m - t (so t = m - k) is F(t) + G(t).

    # But note: t = m - k, so k = m - t.

    # We need to compute F(t) and G(t) for t from 1 to m.

    # How to compute F(t) and G(t) for all t from 1 to m?

    # We can use a Fenwick Tree (Binary Indexed Tree) or a Segment Tree to count inversions.

    # But note: the inversion count for a set of numbers is the same as the inversion count of the entire array for the numbers in that set, but we have to consider the indices.

    # Alternatively, we can use a method that counts the inversion pairs by considering the positions.

    # Idea:

    #   We can sort the array A, but we need to preserve the original indices.

    #   Let's create an array of (A_i, index) and sort by A_i.

    #   Then, for a fixed t, Set1 is all elements with A_i < t, and Set2 is all elements with A_i >= t.

    #   The inversion count for Set1 is the inversion count of the subsequence of A_i < t (with the original indices).

    #   Similarly for Set2.

    #   But note: the inversion condition is defined on the original indices: i < j (in the original sequence) and A_i > A_j.

    #   So, if we have two elements (a, i) and (b, j) with i < j, then if a > b and both are in Set1, then they form an inversion.

    #   We can use a Fenwick Tree to count the number of elements that are greater than a certain value and have appeared before