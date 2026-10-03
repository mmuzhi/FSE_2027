import sys
import math
import heapq

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it)); k = int(next(it))
    functions = []
    for i in range(n):
        a = int(next(it)); b = int(next(it))
        functions.append((a, b))
    
    # Since k is at most 10, we can try to select the best k functions and then order them optimally.
    # But how to choose the best k functions? We need to consider both A and B.
    # We'll use a two-step approach: first, select the top k functions by a criterion, then order them.

    # But note: the value depends on the order. We can use a greedy method to select the best k functions and then sort them by a key.

    # However, the optimal set is not obvious. But note that the product of A's is fixed for the set, and the B's are added with multipliers that are the product of the A's after them.

    # We can use a priority queue to select the best functions. But we need to consider that a function with a very high A might be beneficial even if its B is low, because it will be multiplied by many B's.

    # Alternatively, we can use a state space of k! orders, but k is at most 10, so 10! is 3.6e6, but we have to choose the set first.

    # But the number of ways to choose k functions from 200,000 is too many.

    # Observation: the optimal set must be among the functions with the largest A's and B's. But we cannot be sure.

    # Another idea: use a dynamic programming with state (mask) but mask has 2^k states? No, we need to choose k functions from 200,000.

    # We need a better approach.

    # Let's consider that the value is:
    #   value = (A1 * A2 * ... * Ak) + 
    #           B1 * (A2 * ... * Ak) +
    #           B2 * (A3 * ... * Ak) +
    #           ... +
    #           B_{k-1} * Ak +
    #           Bk

    # We can factor this as:
    #   value = (A1 * (A2 * ... * Ak)) + 
    #           (B1 * (A2 * ... * Ak)) +