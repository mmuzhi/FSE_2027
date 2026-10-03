import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1+n]))
    
    # If the length is 0 or 1, score is 0.
    if n <= 1:
        print(0)
        return
        
    # We'll use dynamic programming.
    # Let dp[i][j] be the maximum score we can get from the subarray A[i:j+1].
    # But n can be up to 300,000, so O(n^2) is too slow.

    # Alternatively, we can use a greedy approach or a stack.

    # Observation: Each element will be removed exactly once, and the score is the absolute difference of the two adjacent elements that are removed together. But note, an element can be part of two removals? No, each removal removes two elements, so each element is removed once.

    # Actually, each element is removed exactly once, and the removal operation is defined by two adjacent elements. So, the entire sequence is partitioned into pairs (each pair is two adjacent elements at the time of removal). But the pairs are not necessarily adjacent in the original sequence because removals can be interleaved.

    # However, note that the removals can be done in any order, so the pairs must be non-overlapping and consecutive in the original sequence? Not necessarily. For example, in [1,2,5,3], we remove (2,5) and then (1,3). The pairs (2,5) and (1,3) are not consecutive in the original sequence, but they are adjacent at the time of removal.

    # Actually, the pairs are not required to be consecutive in the original sequence. But the removal operation requires that the two numbers are adjacent at the time of removal.

    # This is similar to the problem of "removing all parentheses" or "valid bracket matching" but with a scoring function.

    # Another idea: we can use a stack to simulate removals. But how?

    # Alternatively, we can transform the problem: the total score is the sum of absolute differences of the pairs. Each element is used in one pair. The pairs are adjacent at the time of removal, but the adjacency is defined by the current sequence.

    # Let me think of the entire process: we are allowed to remove any two adjacent elements. The total score is the sum of the absolute differences of each removal.

    # This is equivalent to: we are allowed to choose any matching (set of non-overlapping edges) in the sequence graph (a path graph) such that the matching is a set of edges that are adjacent in the current graph. But the removals can be done in any order, so the matching must be a set of edges that form a matching in the original graph? Not exactly, because the adjacency changes.

    # Actually, the problem is equivalent to: we can remove any two adjacent elements, and then the sequence is re-indexed. The total score is the sum of the absolute differences of the removed pairs.

    # This is similar to the problem of "Maximum Independent Set" or "Maximum Matching" but with a scoring function.

    # But note: the removals are not independent. The order matters because the adjacency changes.

    # Let me consider the following: the entire sequence will be removed, and each removal operation removes two adjacent elements. The total number of removals is floor(n/2). The problem is to maximize the sum of absolute differences.

    # We can use a greedy approach: always remove the pair with the maximum absolute difference. But is that optimal?

    # Let's test with the sample [1,2,5,3]:
    # Absolute differences: |1-2|=1, |2-5|=3, |5-3|=2, |1-5|=4 (but 1 and 5 are not adjacent initially). So initially, the adjacent pairs are (1,2), (2,5), (5,3). The maximum is 3 (2,5). Remove them, then the sequence becomes [1,3]. Then remove (1,3) with difference 2. Total 5.
    # Alternatively, if we remove (5,3) first (difference 2), then the sequence becomes [1,2], then remove (1,2) with difference 1, total 3. So greedy by local maximum is not optimal.

    # Another idea: use dynamic programming with state as the current segment and the number of removals. But n is large.

    # Alternatively, we can use a stack-based method. 

    # Observation: The problem is equivalent to: we can remove any two adjacent elements, and the score is the absolute difference. The entire sequence is removed. We want to maximize the total score.

    # This is similar to the problem