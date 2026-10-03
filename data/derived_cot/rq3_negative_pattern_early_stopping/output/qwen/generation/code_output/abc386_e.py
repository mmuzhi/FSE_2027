import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    k = int(data[1])
    A = list(map(int, data[2:2+n]))
    
    # If k is 0, then the XOR is 0, but k>=1 per constraints.
    # Since the binomial coefficient is at most 10^6, we can generate all combinations if k is small or large.
    # But note: generating all combinations of k elements from a list of n elements is not feasible if k is large and n is large, but the total number of combinations is bounded by 10^6.
    # However, we cannot generate all combinations by itertools.combinations because n can be 200000 and k can be 1 or n-1, but the total number of combinations is 10^6, so we can use a different approach.

    # But wait, the problem says the binomial coefficient is at most 10^6, so the total number of combinations is at most 10^6. Therefore, we can use an iterative method that considers all combinations.

    # However, generating all combinations from a list of 200000 elements is not feasible by standard methods because the combinations are subsets and the array is large. But note: the binomial coefficient is the number of combinations, and it is ≤10^6. So the input is such that the number of combinations is small. 

    # But how do we generate all combinations? We don't know the positions. 

    # Actually, the problem does not require us to generate all combinations. We need to find the maximum XOR. 

    # There is a known technique for maximum XOR of a subset (like the maximum subset XOR) using a trie, but that is for subsets of any size. However, here the subset size is fixed to K.

    # But note: the binomial coefficient is small, so we can use a meet-in-middle or other combinatorial search? 

    # Alternatively, we can use the fact that the array elements are non-negative and up to 2^60, and use a greedy bit approach? 

    # However, the problem is fixed-size subset XOR. 

    # Another idea: since the number of combinations is small (≤10^6), we can use a recursive method that iterates over the array and selects K elements, but that would be too slow because the array is large.

    # But wait, the binomial coefficient is the number of combinations, and it is ≤10^6. So we can use an algorithm that enumerates all combinations without explicitly generating all subsets? 

    # Actually, the problem is that the array has 200,000 elements, but the number of combinations is 10^6. So we can use a method that selects combinations without iterating over all 200,000 elements for each combination.

    # We can use a method that uses the fact that the binomial coefficient is small to use a meet-in-middle or dynamic programming? 

    # Alternatively, we can use a method that considers the array as a multiset and uses the small binomial coefficient to our advantage.

    # But note: the binomial coefficient is the number of ways to choose K elements from N. So if we can reduce the problem to a smaller set, we can solve it.

    # However, there is a known technique for the maximum XOR of a subset of fixed size: we can use a recursive search with memoization and a binary trie for the numbers, but that might be too slow.

    # But wait, the binomial coefficient is small (≤10^6). So we can simply iterate over all combinations if we can generate them. But how to generate all combinations of K elements from an array of size N when N is 200,000 and the number of combinations is 10^6? 

    # Actually, we don't need to generate all combinations explicitly. We can use a method that uses the small binomial coefficient to limit the search space.

    # Alternatively, we can use the following approach:

    # Since the binomial coefficient is small, the set of combinations is small. But how do we iterate over all combinations without knowing the indices? 

    # We can use a combinatorial generation algorithm that uses the binomial coefficient to guide the selection. But that is complex.

    # Another idea: use the fact that the binomial coefficient is small to use a brute-force over the combinations. But how to get the combinations? 

    # Actually, the problem does not specify the values of K and N, only that the binomial coefficient is ≤10^6. So we can use a method that works for both small and large K by symmetry: because the problem is symmetric in the sense that