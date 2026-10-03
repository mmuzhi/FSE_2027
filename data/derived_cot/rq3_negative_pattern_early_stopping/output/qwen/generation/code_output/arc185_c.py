import sys
from collections import defaultdict

def main():
    data = sys.stdin.read().split()
    if not data:
        print(-1)
        return
    
    n = int(data[0])
    X = int(data[1])
    A = list(map(int, data[2:2+n]))
    
    # Build a dictionary: number -> list of indices (original indices)
    num_to_indices = defaultdict(list)
    for idx, num in enumerate(A):
        num_to_indices[num].append(idx)
    
    # We'll iterate over each element as the first element (i)
    # For each element A[i], we need to find two elements (j, k) with j > i and k > j such that A[i] + A[j] + A[k] = X.
    # But then, we can fix i and then look for two elements in the subarray [i+1, n-1] that sum to X - A[i].
    # We can use a two-sum method on the subarray [i+1, n-1] for the value (X - A[i]).
    #
    # However, we can precompute a two-sum structure for the entire array and then update it as we move i.
    #
    # Alternatively, we can use a frequency map and then for each i, remove A[i] and then look for two numbers that sum to X - A[i] in the remaining array, but then we have to ensure the indices are > i.
    #
    # But note: the two numbers must be from indices > i.
    #
    # We can do:
    #   Let's create a frequency map for the entire array.
    #   Then, for each i from 0 to n-1:
    #       Let rem = X - A[i]
    #       Then, we need to find two numbers (b, c) such that b + c = rem, and the indices for b and c are > i.
    #       But we have to account for the current element A[i] (if it is b or c, then we need to have at least one more occurrence).
    #
    #   However, we can use the dictionary num_to_indices and for each b, we can check if there is an index > i for b and for c.
    #
    #   But then, we have to iterate over the distinct numbers for each i, which is O(n^2) in the worst-case.
    #
    # Given the constraints, we need an efficient method.
    #
    # Let's try to use a two-pointer method on the entire array (sorted by value) but then recover the original indices.
    #
    # But the condition is on the original indices, not the sorted order.
    #
    # Another idea: 
    #   We can use a two-sum method that uses a set of available numbers (from indices > i) for each i. But then we have to update the set for each i, which is O(n^2).
    #
    # Given the complexity, I'll use the following simpler approach that might work for small n, but not for n=10^6.
    #
    # But the problem requires n up to 10^6.
    #
    # We need to use the following method:
    #   Precompute a dictionary: num_to_indices.
    #   Then, for each i from 0 to n-1:
    #       Let rem = X - A[i]
    #       Let's create a set of available numbers (from indices > i) but then we have to consider duplicates.
    #       But then, we need to find two numbers (b, c) such that b + c = rem and both b and c are in the available set.
    #       But then, we have to account for duplicates.
    #
    #   We can do:
    #       Let's create a frequency map for the subarray [i+1, n-1].
    #       Then, for each number b in the frequency map (which is for indices > i), we check if (rem - b) is in the frequency map.
    #       But then, we have to ensure that if b == rem - b, then the frequency of b is at least 2.
    #       And if b != rem - b, then the frequency of b and rem-b are at least 1.
    #
    #   But then, we have to build the frequency map for the subarray [i+1, n-1] for each i, which is O(n^2).
    #
    # We need to avoid that.
    #
    # Let's try to use a two-pointer method on the entire array (sorted by value) but then recover the original indices.
    #
    # Steps for two-pointer method (three-sum style) on the entire array (without the index condition):