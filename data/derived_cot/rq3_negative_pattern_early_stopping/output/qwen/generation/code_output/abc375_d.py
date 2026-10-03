from collections import defaultdict

def main():
    S = input().strip()
    # Group indices by character
    char_positions = defaultdict(list)
    for idx, char in enumerate(S):
        char_positions[char].append(idx)
    
    total_triples = 0
    for char, positions in char_positions.items():
        n = len(positions)
        if n < 2:
            continue
        # Calculate the sum of the first j elements for j from 0 to n-1
        prefix = [0] * n
        prefix[0] = positions[0]
        for i in range(1, n):
            prefix[i] = prefix[i-1] + positions[i]
        
        # Now, for each j (from 1 to n-1), we want to compute:
        # Sum_{i=0}^{j-1} (positions[j] - positions[i] - 1) for each j
        # But note: the entire expression for the character is the sum over all pairs (i, j) (i<j) of (positions[j] - positions[i] - 1)
        # We can break it down: 
        #   = Sum_{j=1}^{n-1} [ (positions[j] * j) - (sum_{i=0}^{j-1} positions[i]) ] - (number of pairs) * 1
        # But note: the term (positions[j] - positions[i] - 1) for a fixed j and i is (positions[j] - positions[i] - 1)
        # So the entire sum is:
        #   Sum_{j=1}^{n-1} [ (positions[j] * j) - (prefix[j-1]) ] - (n*(n-1)//2)
        #
        # However, wait: the expression (positions[j] - positions[i] - 1) for each pair (i, j) is being summed. 
        # We can compute the sum of (positions[j] - positions[i]) for all pairs and then subtract the number of pairs (which is n*(n-1)//2).
        #
        # But note: the problem requires the triple (i, j, k) and the condition is that the substring is a palindrome, which is equivalent to S[i]==S[k]. 
        # And we are counting for each character the pairs (i, k) (with i < k) and then for each such pair, the number of j is (k - i - 1). 
        # So the total for the character is the sum_{i<k} (k - i - 1) = (sum_{i<k} k) - (sum_{i<k} i) - (number of pairs)
        #
        # But note: the pairs (i, k) are the same as the pairs (i, j) in the above? Actually, in our grouping, we are considering the positions of the same character. 
        # And the condition is that the first and last are the same character. The middle j must be between i and k (and also of any character). 
        # However, note: the triple (i, j, k) must have i < j < k. And we are counting for each pair (i, k) (with i and k being positions of the same character) the number of j's that lie between i and k. 
        # But j must be an index in the string and also between i and k. However, note that j can be any index (not necessarily the same character) as long as it is between i and k. 
        #
        # But wait: the above grouping by character only considers the positions of the same character for i and k. Then the j can be any index between i and k, regardless of character. 
        # So the count for a fixed pair (i, k) is (k - i - 1). 
        #
        # Therefore, the total for the character is the sum_{i<k} (k - i - 1) = (sum_{i<k} k) - (sum_{i<k} i) - (number of pairs)
        #
        # We can compute:
        #   Let A = sum_{i<k} k = for each k (from 0 to n-1) we add k (the position) multiplied by the number of i's that are less than k (which is k, because i from 0 to k-1) -> but wait, the list L is the positions of the character, and we are considering pairs (i, k) where i and k are indices in the list (so the actual positions are L[i] and L[k]). 
        #
        # Actually, we are grouping by the character, and the positions are the actual indices in the string. 
        #