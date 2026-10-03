import sys
from collections import defaultdict

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    if not data:
        print(0)
        return
        
    it = iter(data)
    n = int(next(it)); m = int(next(it))
    conditions = []
    for _ in range(m):
        L = int(next(it)); R = int(next(it)); X = int(next(it))
        conditions.append((L, R, X))
        
    # We are going to use DP with state as the mask of used elements? But n=500, so mask is 2^500 which is too big.

    # Alternatively, we can use the idea of "inclusion-exclusion" but with state DP that tracks the positions of the maximums? 

    # Actually, note: the conditions are independent in the sense that each condition is about a segment and a position. 

    # Another idea: use the fact that the maximum in a segment must be one of the elements, and we can use a DP that goes from left to right and assigns numbers, but we need to track the maximums in segments. 

    # But note: the conditions are about the maximum not being at a specific position. We can rephrase: for each condition (L, R, X), the element at X must not be the maximum in [L, R]. 

    # Let's consider the following: the maximum in [L, R] is the largest element in that segment. So, if we assign numbers to positions, then for each condition, the element at X must be less than at least one element in [L, R] (which is not at X). 

    # But note: the condition is automatically satisfied if the maximum of [L, R] is not at X. 

    # We can use a different approach: count the permutations that satisfy all conditions by ensuring that for each condition, the element at X is not the maximum in [L, R]. 

    # However, with M up to 100,000, we cannot check each condition individually for each permutation.

    # Another idea: use the principle of inclusion-exclusion but with a smarter way to count the violating permutations. But the state space is too large.

    # Alternatively, we can use a DP that goes from left to right and assigns numbers, and we keep track of the positions of the maximums in the segments that are defined by the conditions. But that seems too vague.

    # Wait, note: the conditions are given as (L, R, X). We can precompute for each position X, the conditions that involve X. But that doesn't help.

    # Let me think about the constraints: N=500, M=100,000. The sample inputs are small, but worst-case M is 100,000. 

    # Another idea: use the fact that the conditions are about the maximum in a segment. The maximum in a segment is the largest element in that segment. So, if we assign the numbers from 1 to N, then the maximum in a segment is the largest number in that segment. 

    # We can use a DP that assigns numbers from 1 to N to positions, and we keep track of the current maximums in the segments that are defined by the conditions. But that is too vague.

    # Alternatively, we can use a segment tree to keep track of the maximums, but then how to count the permutations?

    # Wait, there's a known approach for counting permutations with forbidden positions (like derangements) but here the forbidden positions are conditional on the segment.

    # Another idea: use the principle of inclusion-exclusion but with a state that is the set of conditions that are violated. But 100,000 conditions is too many.

    # Alternatively, we can use a DP that goes from left to right and assigns numbers, and we keep track of the positions of the elements that are the maximums in the segments that end at the current position. But that seems too complex.

    # Let me try to reframe: We need to count the permutations P such that for each condition (L, R, X), the element at X is not the maximum in [L, R]. 

    # This is equivalent to: for each condition, the element at X is less than at least one element in [L, R] (which is not at X). 

    # But note: the condition is automatically satisfied if the element at X is not the maximum. 

    # We can use a DP that assigns numbers from 1 to N to positions, and we keep track of the current maximums in the segments that are defined by the conditions. But that is too vague.

    # Wait, note: the conditions are independent in the sense that they are about