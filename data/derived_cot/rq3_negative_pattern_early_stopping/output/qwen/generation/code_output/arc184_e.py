import sys
from collections import defaultdict

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    it = iter(data)
    n = int(next(it)); m = int(next(it))
    seqs = []
    for _ in range(n):
        a = [int(next(it)) for _ in range(m)]
        seqs.append(a)
    
    # Precompute the transformation T^x for x in a cycle? But note: the transformation is linear and invertible, so the state space is finite (2^m) and the transformation is a permutation. We can find the cycle for each distinct vector.

    # However, note: we are not iterating over all vectors, but over the given sequences. But we need to compute for each pair (i, j) the smallest x such that T^x (seqs[i]) = T^x (seqs[j]), which is equivalent to T^x (seqs[i] + seqs[j]) = 0.

    # But wait, the condition is T^x (seqs[i]) = T^x (seqs[j]), which is T^x (seqs[i] + seqs[j]) = 0. And since T is invertible, T^x is invertible, so the only solution is when seqs[i] + seqs[j] is in the kernel of T^x. But the kernel is {0} only if T^x is invertible. But wait, T is invertible, so T^x is invertible, so the kernel is {0}. Therefore, the condition is that seqs[i] + seqs[j] = 0, i.e., seqs[i] == seqs[j]. 

    # But that contradicts the sample. 

    # Let me reexamine the operation. 

    # The operation is: for each k, set A_{i,k} = (sum_{l=1}^{k} A_{i,l}) mod 2.

    # Let me denote the transformation as T. Then T is a linear transformation. 

    # Now, consider two sequences a and b. We want T^x(a) = T^x(b). 

    # This is equivalent to T^x(a - b) = 0. 

    # But in GF(2), subtraction is addition. So T^x(a + b) = 0.

    # But if T^x is invertible, then a + b must be 0. 

    # However, the sample shows that sometimes a != b but after some x, T^x(a) = T^x(b). 

    # This implies that T^x is not invertible? But wait, T is invertible, so T^x is invertible. 

    # Wait, unless the operation is not invertible? 

    # Let me check the invertibility of T. 

    # The matrix T is:
    # [1 0 0 ... 0]
    # [1 1 0 ... 0]
    # [1 1 1 ... 0]
    # ...
    # [1 1 ... 1]

    # The determinant of T is 1 (product of diagonals) and since we are in GF(2), 1 is invertible. So T is invertible. 

    # But then T^x is invertible, so the only vector that maps to 0 is 0. 

    # So the condition T^x(a) = T^x(b) is equivalent to a = b. 

    # But the sample says otherwise. 

    # There must be a misunderstanding. 

    # Let me recast the problem: 

    # We are allowed to apply the operation x times. The operation is defined as: 
    #   For each k from 1 to M: A_{i,k} becomes the cumulative sum from 1 to k mod 2.

    # But note: the operation is applied to each sequence independently. 

    # Now, consider two sequences a and b. We want to know if there exists an x such that after x operations, a and b become the same. 

    # But note: the operation is deterministic and linear. 

    # Let me compute T^2 for a small example. 

    # Let a = [a1, a2, a3]. Then T(a) = [a1, a1+a2, a1+a2+a3].
    # Then T^2(a) = T(T(a)) = [a1, a1 + (a1+a2), a1 + (a1+a2) + (a1+a2+a3)] 
    # = [a1, (a1 + a1 + a2), (a1 + a1 + a2 + a1 + a2