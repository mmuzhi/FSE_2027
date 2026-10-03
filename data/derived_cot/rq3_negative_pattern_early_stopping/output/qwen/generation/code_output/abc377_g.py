import sys

def main():
    data = sys.stdin.read().splitlines()
    n = int(data[0])
    strings = []
    for i in range(1, n+1):
        strings.append(data[i].strip())
    
    # We'll store the answers for each k
    ans = []
    
    # We are going to use a trie to store all the previous strings (for k>=2, we store S_1 to S_{k-1})
    # But note: we also have the option of making T empty. The cost for empty is len(T).
    # So for each T, we need to consider the minimal cost over all previous strings (or empty) and the empty string.
    # The empty string is a special case: we can delete all characters (cost = len(T)).
    # But note: the empty string is not in the previous strings (unless k=1, then there are no previous strings, so we must use empty).
    # However, for k>=2, we have previous strings and the empty string is also an option.

    # We can precompute the minimal cost for each T by considering:
    #   Option 1: Delete all (cost = len(T))
    #   Option 2: For each previous string U, compute the cost as described.

    # But the total length is 200,000, and N can be 200,000, so we cannot iterate over all previous strings for each T.

    # We need an efficient way.

    # Observation: The cost for transforming T to U is:
    #   Let n = len(T), m = len(U)
    #   Let L = the length of the longest common prefix between T and U (but note: we can only delete from T, so we are matching T's prefix with U's prefix).
    #   Actually, we are matching T's prefix (of length L) with U's prefix (of length L). Then the cost is 2*(n - L) + (m - (n - L))? 
    #   Wait, no: we delete (n - L) characters from T (so that the remaining is T[0:L]), then we add (m - L) characters to get U.
    #   So the cost is (n - L) + (m - L) = n + m - 2*L.

    # But wait, let me check with the sample:
    #   T = "snuki", U = "snuke": 
    #       n=5, m=5, L=4 (common prefix "snu")
    #       cost = 5+5-8 = 2. Correct.
    #   T = "snuuk", U = "snuki":
    #       n=5, m=5, L=3 (common prefix "snu")
    #       cost = 5+5-6 = 4. Correct.
    #   Also, for T="abc", U="axc": 
    #       n=3, m=3, L=1 (common prefix "a")
    #       cost = 3+3-2=4.

    # But wait, is that always the case? 

    # Actually, the transformation is: 
    #   We delete (n - L) characters from T, then add (m - L) characters. 
    #   So the cost is (n - L) + (m - L) = n + m - 2*L.

    # And for the empty string: 
    #   We delete all n characters, so cost n. 
    #   Alternatively, we can think of the empty string as having length 0, and the common prefix L=0, then cost = n + 0 - 0 = n. 

    # So the formula for the empty string is included.

    # Therefore, for a given T and a set of previous strings (and the empty string), the minimal cost is:
    #   min( len(T),  min_{U in previous strings} (len(T) + len(U) - 2 * LCP(T, U)) )

    # But note: we can also consider that the empty string is always an option, and the cost for empty is len(T). 

    # Now, the challenge is to compute this efficiently for each T (each string S_k) and for all previous strings (S_1 to S_{k-1}).

    # We have up to 200,000 strings, and the total length is 200,000. 

    # We need to compute the Longest Common Prefix (LCP) between T and every previous string. 

    # We can use a trie to store all the previous strings and then for T, we traverse the trie to get