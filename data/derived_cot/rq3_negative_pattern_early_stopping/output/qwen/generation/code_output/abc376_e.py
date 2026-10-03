import sys
from bisect import bisect_left, bisect_right

def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    index = 1
    results = []
    
    for _ in range(t):
        N = int(data[index]); index += 1
        K = int(data[index]); index += 1
        A = list(map(int, data[index:index+N])); index += N
        B = list(map(int, data[index:index+N])); index += N
        
        # Combine and sort by A
        arr = sorted(zip(A, B), key=lambda x: x[0])
        # Group by A
        groups = {}
        for a, b in arr:
            if a not in groups:
                groups[a] = []
            groups[a].append(b)
            
        # Get distinct A values in sorted order
        distinct_ain = sorted(groups.keys())
        
        # We'll maintain a Fenwick tree or segment tree for the B_i's? 
        # But note: the total N is up to 200,000, but the total over test cases is 200,000, so we can do a two-pointer and a sorted list for T.
        # Alternatively, we can use a balanced BST for the entire set T (all elements with A_i <= x) and then use a Fenwick tree for the B_i's? 
        # But note: we are iterating x, and T is increasing. We can use a two-pointer and a sorted list for T and then use binary search to get the K-th smallest.
        
        # We'll maintain:
        #   T_list: the list of B_i's for all elements with A_i <= x (for the current x)
        #   We'll also maintain a Fenwick tree for the B_i's? Or we can use a balanced BST and then use a heap for the smallest K elements.
        #
        # However, note: the total N is 200,000, and the total over test cases is 200,000, so we can do a two-pointer and a sorted list for T and then use a Fenwick tree for the entire array? 
        #
        # Actually, we can do:
        #   We'll iterate x from the smallest distinct A_i to the largest.
        #   We'll maintain a list T_list (the B_i's for all elements with A_i <= x) and also a Fenwick tree for the B_i's? 
        #
        # But note: the condition is that we must have at least one element from the current x (the set S2). 
        #
        # We can do:
        #   Let T_list be the list of B_i's for all elements with A_i <= x (we'll append the current group's B_i's).
        #   Then, we want to compute the minimal sum of K elements from T_list that includes at least one element from the current group (groups[x]).
        #
        #   We can precompute the minimal sum of K elements from T_list (without condition) by sorting T_list and taking the first K? But T_list is not sorted by B_i.
        #
        #   Alternatively, we can maintain a sorted list for T_list and then use a Fenwick tree for the B_i's? 
        #
        #   But note: the total number of elements is N (<=200,000) and the total over test cases is 200,000, so we can do a two-pointer and a sorted list for T_list and then use a Fenwick tree for the entire array? 
        #
        #   Actually, we can do:
        #       We'll maintain a sorted list for T_list (the B_i's) and then use bisect to get the K-th smallest.
        #
        #   Steps for a fixed x:
        #       Add all B_i's from groups[x] to T_list.
        #       Then, we want to find the minimal sum of K elements from T_list that includes at least one element from groups[x].
        #
        #   We can do:
        #       Let total = the sum of the smallest K elements in T_list (without condition).
        #       Let count = the number of elements in the smallest K elements that are from groups[x].
        #       If count >= 1, then candidate = x * total.
        #       Else, then we need to replace the largest element in the smallest K (which is the K-th smallest) with the smallest element from groups[x] (which is the smallest B_i in groups[x]).
        #           candidate = x * (total - T_list_sorted[K-1] + min(groups[x]))
        #
        #   But wait: what if the smallest K elements in T_list do not include