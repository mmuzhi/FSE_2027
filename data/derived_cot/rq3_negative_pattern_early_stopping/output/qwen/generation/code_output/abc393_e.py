import sys
from collections import defaultdict
import math

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    k = int(data[1])
    A = list(map(int, data[2:2+n]))
    
    # If k == 1, then answer for each is the number itself, but we have to consider that the set is just one element, so GCD is the element itself.
    # But note: the problem says "choose K elements", so for k=1, we choose one element, and the GCD is that element.
    # However, the problem requires that the chosen set includes A_i, so for k=1, the answer is A_i.

    # But note: the constraints say K at most N, and N can be 1.2e6, so we need an efficient solution.

    # We are going to use the following idea:
    # For each divisor d, let's count the frequency of numbers divisible by d, but we need to consider the entire array.

    # However, we are required to output the answer for each A_i.

    # Alternate approach:
    # 1. Precompute the frequency of each number and its multiples.
    # 2. For each divisor d, we can consider the set S_d of numbers divisible by d.
    # 3. Then, we can compute the GCD of the entire set S_d? Not exactly, but we can compute the GCD of the set of numbers in S_d that are divisible by d, but then we can use the fact that the GCD of S_d is the GCD of all numbers in S_d.

    # But note: the maximum GCD we can get from a set of numbers is the GCD of the set. So, for a fixed d, the maximum GCD we can get from a set of numbers divisible by d is the GCD of the set of numbers in S_d? Not necessarily, because we can choose a subset of S_d that has a higher GCD than the GCD of S_d.

    # Actually, the GCD of a subset of S_d must be a multiple of d. And the maximum GCD we can get from S_d is the maximum value g (multiple of d) such that there are at least K numbers in S_d that are divisible by g.

    # So, for each divisor d, we can consider the set S_d. Then, for each multiple g of d, we can check how many numbers in S_d are divisible by g. But that is too heavy.

    # Another idea: use the concept of "multiple counting" and "Mo's algorithm" or "two pointers"? Probably not.

    # Let me think from the perspective of the answer. The answer for A_i is the maximum g such that there exists a subset of K elements including A_i, and g divides every element in the subset.

    # We can rephrase: g must divide A_i, and also divide the other K-1 elements. So, g must be a divisor of A_i.

    # So, for each A_i, we can consider all divisors of A_i. Then, for each divisor d of A_i, we can check: how many numbers in the entire array (including A_i) are divisible by d? If that count is at least K, then d is a candidate. But note, we need to choose K elements including A_i, so the count must be at least K, and we can choose A_i and K-1 others from the numbers divisible by d.

    # However, the candidate d is just a divisor, but the actual GCD of the chosen set might be a multiple of d. But we are looking for the maximum GCD. So, we want the maximum g (which is a divisor of A_i) such that there are at least K numbers in the array divisible by g.

    # But wait, that is not correct. Because if we choose a set with GCD g, then g must divide every element, so g must divide A_i. So, the answer for A_i must be a divisor of A_i. Therefore, we can consider only the divisors of A_i.

    # Then, the problem reduces to: for each A_i, find the maximum divisor d of A_i such that the number of elements in A divisible by d is at least K.

    # But wait, is that sufficient? Let me check with the sample: 
    # Input: 5 2
    #        3 4 6 7 12
    # For A_1=3: divisors are 1,3. 
    #   d=1: count numbers divisible by 1: 5 >=2 -> candidate 1.
    #   d=3: count numbers divisible by 3: 3,6,12 -> 3 >=