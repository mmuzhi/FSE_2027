import sys
from functools import lru_cache

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    a = list(map(int, data[1:1+n]))
    total = sum(a)
    # We are going to use a DP over the bags and the XOR value and the total stones in each bag?
    # But note: the problem constraints: N up to 12, and A_i up to 10^17, so we cannot iterate over all possible sums (which can be huge).
    # Instead, we can use the fact that the final configuration is an assignment of each original bag to one of the N bags (the final bag). 
    # But note: the operation requires that we move each bag at most once, and the assignment must be such that the set of bags that are assigned to a final bag must be a partition of the original bags (each original bag is assigned to exactly one final bag). 
    # However, the operation doesn't require that the assignment is a partition: because we can move a bag's stones to a bag that is then moved again. But note: the stones from a bag are moved only once (when the bag is moved). 
    # Actually, the assignment is: each original bag i is assigned to a final bag j (the bag that ends up with its stones). And the assignment must be such that the set of bags that are assigned to a final bag j is arbitrary, but the assignment must be a function from {1,...,N} to {1,...,N}. 
    # But note: the operation allows us to move a bag's stones to any bag, so we can assign independently. 
    # Therefore, the problem reduces to: count the number of distinct values of the XOR of the final bag contents, where the final bag j has the sum of the original bags i that are assigned to j. 
    # However, the assignment must be such that the set of bags that are assigned to a final bag is arbitrary, but note: the operation requires that we move each bag at most once, and the assignment must be such that the set of bags that are assigned to a final bag is exactly the set of bags that are not emptied? Actually, no: because we can move a bag's stones to a bag that is then moved again. 
    # Let me reframe: 
    # We have N bags. We can perform operations that move all stones from one bag to another. Each operation empties the source bag. 
    # The final configuration is determined by a set of non-empty bags (each non-empty bag is the union of some original bags) and the rest are empty. 
    # But note: the operation doesn't require that the destination bag is empty. So, we can merge multiple bags into one. 
    # The key is: the final configuration is a partition of the set of original bags into up to N non-empty subsets (each subset is assigned to a bag, and the bag's value is the sum of the subset). 
    # However, note: the bags are labeled. So, the assignment is: we assign each original bag to one of the N bags (the final bag). Then, the final bag j has the sum of the original bags assigned to j. 
    # But wait, is that correct? Consider: 
    #   Operation 1: move bag1 to bag2: then bag2 has A1+A2, bag1=0.
    #   Operation 2: move bag3 to bag2: then bag2 has A1+A2+A3, bag3=0.
    #   Operation 3: move bag4 to bag1: then bag1 has A4, bag4=0.
    # Then, the assignment is: bag1: {4}, bag2: {1,2,3}, bag3: {}, bag4: {}.
    # But note: the operation moved bag1 and bag3 to bag2, and bag4 to bag1. 
    # So, the assignment is: each original bag is assigned to one final bag. 
    # Therefore, the problem is: count the number of distinct values of the XOR of the final bag contents, where the final bag j has the sum of the original bags i that are assigned to j. 
    # But note: the assignment is a function from {1,...,N} to {1,...,N}. There are N^N possible assignments. But N is up to 12, so 12^12 is about 8 billion, which is too many to iterate. 
    # However, we can use dynamic programming with state as a bitmask of which original bags have been assigned and the current XOR value? But the XOR value can be up to 10^17, which is too big. 
    # Alternatively, we can use the fact that