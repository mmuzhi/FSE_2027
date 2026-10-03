import sys
from math import comb

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    m = int(data[1])
    k = int(data[2])
    X = list(map(int, data[3:3+m]))
    
    # We'll compute the answer modulo 998244353
    mod = 998244353

    # If M == 1, then the condition is that the only sequence of length 1 that is not present is X.
    # But note: the problem states M>=2, so we don't need to handle M=1.
    # However, the constraints say M>=2, so we can assume M>=2.

    # But wait, the sample input has M=2, so we are safe.

    # The problem is non-trivial. We need to count sequences A of length N (with elements 1..K) such that:
    #   - Every sequence of length M except X is a subsequence of A.
    #   - X is not a subsequence of A.

    # This is a very hard problem. 

    # However, note that the sample input 5 2 3 [1,1] gives 4.

    # Let me reexamine the sample: 
    #   N=5, M=2, K=3, X=[1,1]
    #   The valid sequences are those that have exactly one 1, and the rest are 2's and 3's, but arranged in such a way that the 1 is not the only element and that the two 2's and two 3's are arranged so that the 1 is not the first and not the last? Actually, no.

    # Actually, the sample sequences are:
    #   (2, 3, 1, 2, 3)
    #   (2, 3, 1, 3, 2)
    #   (3, 2, 1, 2, 3)
    #   (3, 2, 1, 3, 2)

    # These sequences have the 1 at position 3. The first two elements are a permutation of [2,3] and the last two are the other permutation.

    # So, the pattern is: the 1 is fixed at position 3, and the first two positions are filled with 2 and 3 (in any order) and the last two positions are filled with the remaining numbers (again in any order). But wait, the last two positions must be the same as the first two but in reverse order? Actually, no: in the first sequence, first two are [2,3] and last two are [2,3] again. In the second, first two [2,3] and last two [3,2]. In the third, first two [3,2] and last two [2,3]. In the fourth, first two [3,2] and last two [3,2].

    # Actually, the condition is that the 1 must be at a position such that there is at least one 2 and one 3 before it (to form [2,1] and [3,1]) and at least two 2's and two 3's in total (to form [2,2] and [3,3]). But wait, [2,2] requires two 2's. In the sample sequences, there are two 2's and two 3's.

    # So, the sequence A must have:
    #   - Exactly one 1.
    #   - At least two 2's.
    #   - At least two 3's.

    # But the total length is 5, so the counts must be: 1 one, 2 twos, 2 threes.

    # Now, the number of sequences with one 1, two 2's, two 3's is: 
    #   C(5,1) * C(4,2) * C(2,2) = 5 * 6 * 1 = 30.

    # But the sample output is 4.

    # So, clearly, not every arrangement of one 1, two 2's, two 3's is valid.

    # Why? Because we must be able to form every pair except [1,1]. 

    # Consider a sequence with one 1, two 2's, two 3's, but the 1 is at the beginning. Then, we cannot form [2,1] because there is no 2 before the 1. Similarly, if the 1 is at the end, then we can form [2,1] and [3,1] because there