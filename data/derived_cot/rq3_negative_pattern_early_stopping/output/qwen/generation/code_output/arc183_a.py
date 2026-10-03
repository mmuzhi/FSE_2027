import math
from math import factorial

def main():
    import sys
    data = sys.stdin.read().split()
    N = int(data[0])
    K = int(data[1])
    total_length = N * K
    # If K == 1, then the sequence is just the numbers 1 to N, but in lexicographical order, 
    # the sequences are just the permutations of 1 to N. But wait, no: each number appears once, so the sequence is the permutation of 1 to N. 
    # The number of sequences is factorial(N). Then we need the (factorial(N)+1)//2-th permutation.
    # But note: the sample input "6 1" gives "3 6 5 4 2 1". 
    # Actually, for N=6, K=1, the total sequences are 720. The (720+1)//2 = 360.5 -> 360th sequence (if 1-indexed). 
    # But wait, the sample output is "3 6 5 4 2 1". 
    # Let me check: the lexicographical order for permutations of [1,2,3,4,5,6] is from (1,2,3,4,5,6) to (6,5,4,3,2,1). 
    # The 360th permutation (if we consider 1-indexed and the first being 1) is the 359th in 0-indexed. 
    # But the sample output is "3 6 5 4 2 1". 
    # Actually, the sample input "6 1" is provided and the output is "3 6 5 4 2 1". 
    # So we need to generate the 360th permutation (1-indexed) of [1,2,3,4,5,6]. 
    # But wait, the problem says: "Find the floor((S+1)/2)-th good integer sequence in lexicographical order."
    # For N=6, K=1, S = 720, so floor((720+1)/2)=360. So the 360th sequence (1-indexed). 
    # The 360th permutation (1-indexed) is the 359th in 0-indexed. 
    # The standard way to generate the k-th permutation is to use factorial numbering. 
    # But note: the lexicographical order of permutations is defined by the usual order. 
    # The first permutation is [1,2,3,4,5,6], the second is [1,2,3,4,6,5], etc. 
    # The 360th permutation (1-indexed) is the 359th in 0-indexed. 
    # We can generate the k-th permutation by: 
    #   k = k - 1 (to make it 0-indexed)
    #   Then for each position, choose the element from the remaining set by dividing k by the factorial of the remaining length-1. 
    # But note: our sequence is a permutation of 1 to N, each appearing once. 
    # However, the problem is more general: we have each number from 1 to N appearing K times. 
    # So the general case is a multiset permutation. 
    # But the sample input "2 2" gives "1 2 2 1". 
    # So we need a general solution that works for any N and K up to 500. 
    # The total length is N*K, which can be up to 250000. 
    # We cannot generate all sequences. 
    # We need to use a combinatorial counting method. 
    # The idea: 
    #   We have a multiset of numbers: each number i from 1 to N has count K. 
    #   We want the (S+1)//2-th sequence in lexicographical order. 
    #   We can use a recursive method: 
    #       At each step, consider the next position. 
    #       For each candidate number (from 1 to N) that still has remaining copies, 
    #           count the number of sequences that start with that candidate. 
    #       Then, if the desired sequence index is within the count for candidate x, then we choose x and reduce its count by 1. 
    #       Otherwise, subtract the count and move to the next candidate. 
    #   The challenge is to compute the count for a given candidate without calculating huge factorials. 
    #   The