import sys

def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    index = 1
    results = []
    for _ in range(t):
        n = int(data[index]); index += 1
        arr = list(map(int, data[index:index+2*n]))
        index += 2*n
        
        # Precompute the positions for each number
        pos = {}
        for i, num in enumerate(arr):
            if num not in pos:
                pos[num] = []
            pos[num].append(i)
        
        # We are only concerned with numbers from 1 to n, each appears twice.
        # Conditions for a pair (a, b) (a < b):
        #  1. The two occurrences of a are not adjacent.
        #  2. The two occurrences of b are not adjacent.
        #  3. The four positions (the two of a and two of b) can be rearranged (by swapping a and b arbitrarily) so that the two a's are adjacent and the two b's are adjacent.
        #
        # Condition 3 is equivalent to: the four positions (p1, p2 for a and q1, q2 for b) must contain two disjoint pairs of consecutive indices (i.e., there are two pairs (x, x+1) and (y, y+1) such that {x, x+1} and {y, y+1} are subsets of the four positions, and the two pairs are disjoint).
        #
        # However, note: the four positions are fixed. We can assign the two a's to two adjacent indices and the two b's to two adjacent indices. But the four indices must form two consecutive pairs. But note: the consecutive pairs must be in the entire array. So the four indices must include two consecutive pairs (which might be overlapping? No, because we have four distinct indices). Actually, the two consecutive pairs must be disjoint and each of size two, so they form two adjacent pairs that are not overlapping.
        #
        # But note: the four indices might be consecutive in a block of four? For example, [i, i+1, i+2, i+3]. Then we can split them into (i, i+1) and (i+2, i+3). Or [i, i+1, i+2, i+3] can also be split into (i, i+1) and (i+1, i+2) but that would use i+1 twice, which is not allowed because we have distinct indices. So we need two disjoint consecutive pairs.
        #
        # Alternatively, we can think: the four indices must form two adjacent pairs (each pair being two consecutive indices) and the two pairs are disjoint. Then the four indices must be either:
        #   Case 1: Two separate adjacent pairs (like [i, i+1, j, j+1] with j >= i+2).
        #   Case 2: Or, they form a block of four consecutive indices (like [i, i+1, i+2, i+3]) and then we can split into (i, i+1) and (i+2, i+3) OR (i, i+1) and (i+1, i+2) is not allowed because the pairs must be disjoint. Actually, in a block of four consecutive indices, we can only split into two disjoint pairs if we take (i, i+1) and (i+2, i+3). The other way (i, i+1) and (i+1, i+2) is not disjoint.
        #
        # So the condition is: the four indices must be able to be partitioned into two pairs of consecutive indices (each pair being two consecutive indices) and the two pairs are disjoint.
        #
        # How to check for a given set of four indices (p, q, r, s) (sorted) whether they can be split into two consecutive pairs?
        # Let the sorted indices be [x, y, z, w]. Then we require:
        #   Either:
        #     (x, y) is consecutive and (z, w) is consecutive, and y+1 = z (so they are adjacent) is not necessary, but we just need two consecutive pairs. Actually, the two consecutive pairs can be anywhere in the array, not necessarily adjacent to each other.
        #   But note: the consecutive pairs are defined by the entire array's index order. So we just need two pairs (each of two consecutive indices) that are subsets of {x, y, z, w}. And the two pairs must be disjoint (so four distinct indices).
        #
        # Example: [1, 2, 4, 5] -> (1,2) and (4