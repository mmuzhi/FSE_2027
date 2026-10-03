import sys
from collections import deque

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    index = 1
    out_lines = []
    
    for _ in range(t):
        n = int(data[index]); index += 1
        p_list = list(map(int, data[index:index+n])); index += n
        a_list = list(map(int, data[index:index+n])); index += n
        
        # Build the tree (children list)
        children = [[] for _ in range(n+1)]
        for i in range(1, n+1):
            parent = p_list[i-1]
            children[parent].append(i)
            
        # Total sum of a_i
        total_a = sum(a_list)
        # Normalize the probabilities: but we'll use modular inverses for mod arithmetic
        # We'll compute the expected value modulo 998244353
        
        # We need to compute the expected number of operations. We can use a DFS to compute the expected time for each node.
        # Let dp[u] be the expected number of operations to find the treasure starting from node u (assuming u is already searched and we haven't found the treasure yet) but wait, actually we need to consider the entire process from the root.
        # Alternatively, we can use the concept: the expected operations is the sum over all nodes of (probability that the node is visited before the treasure) but that is not exactly the same because we stop at the treasure.
        # Actually, the process is: we start at root (0) and then we choose an unsearched vertex with a searched parent. The operation count is the number of nodes we mark until we hit the treasure.
        # We can think of the expected operations as the sum over all nodes (except the treasure) of the probability that we visit that node, but that is not correct because the process stops at the treasure.
        # Actually, the expected operations is the sum over all nodes of the probability that the node is the first one to be searched (if it's the treasure) or the probability that we search that node (if it's not the treasure) but wait, no: the operation count is the number of operations until the treasure is found. So if the treasure is found at node u, then we have performed (depth of u in the search tree) operations? Not exactly: the operations are the nodes we mark, and the order is chosen optimally.

        # Let me define:
        # Let f(u) be the expected number of operations to find the treasure, given that we are at node u (and u is the current root of the subtree we are considering, and we haven't found the treasure yet). But actually, we are at the root (vertex 0) initially.

        # However, note that the process is defined from the root and we can choose the order of children. The optimal strategy is to search the child with the highest probability first, then next, etc.

        # Actually, we can use a greedy approach: for each node, the expected operations to find the treasure in its subtree is the sum of the probabilities of the nodes in the subtree (but normalized by the total probability of the subtree) times the time it takes to reach them.

        # Alternatively, we can use the following idea:
        # Let P(u) be the probability that the treasure is in the subtree rooted at u (including u). Then, the expected operations to find the treasure in the subtree of u, if we are at u, is the sum over the children of u of (their expected operations) but weighted by the order.

        # Actually, the standard solution for such problems is to use a DFS and compute the expected operations for each node.

        # Steps:
        # 1. Compute the probability for each node: the probability that the treasure is in the subtree rooted at u is the sum of a_i for i in the subtree, divided by the total sum (but we can use modular arithmetic).

        # 2. Then, the expected operations from node u is the sum over its children of (expected operations from child) but we must account for the order.

        # However, note: the process stops when the treasure is found. So if we are at node u, and we haven't found the treasure, then we must search all nodes until we hit the treasure.

        # But the optimal strategy is to search the children in descending order of their probability (or the probability of the treasure being in their subtree). Then, the expected operations from u is:

        # Let the children of u be c1, c2, ..., ck, and let P_i = probability that the treasure is in the subtree of c_i (including c_i). Then, the expected operations from u is the sum over i of (P_i * (1 + expected operations from c