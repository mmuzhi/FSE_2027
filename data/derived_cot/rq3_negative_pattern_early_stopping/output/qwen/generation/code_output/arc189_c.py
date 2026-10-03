import sys
from collections import deque

def main():
    data = sys.stdin.read().split()
    it = iter(data)
    n = int(next(it)); X = int(next(it))
    A = [int(next(it)) for _ in range(n)]
    B = [int(next(it)) for _ in range(n)]
    P = [int(next(it)) - 1 for _ in range(n)]
    Q = [int(next(it)) - 1 for _ in range(n)]
    
    # If the total red and blue are already in the X-th box, then we might need 0 operations.
    # But note: the goal is to have all boxes except X empty. So if the X-th box has the total red and blue, then we are done.

    total_red = sum(A)
    total_blue = sum(B)
    
    # The X-th box (index X-1) must have total_red and total_blue at the end.
    # But note: the operations are reversible in terms of routing? Actually, we need to check if we can route all red to X and all blue to X.

    # However, note: the operations are defined by two permutations. We can model the problem as a flow in a graph with two separate graphs (for red and blue) but note: the operation is defined by the same box index for both.

    # Actually, we can consider two separate graphs: one for red and one for blue.

    # For red: we have a directed graph with n nodes and edges i -> P[i] for each i.
    # For blue: i -> Q[i] for each i.

    # The problem for red: we have an initial distribution of red balls (A[i] for each box i). We can remove from a box and send to P[i]. We can do operations repeatedly. We wish to have all red balls in the X-1 box.

    # Similarly for blue.

    # But note: the operations are not limited to one time per box. We can use a box multiple times.

    # However, the graph for red is a permutation graph (each node has out-degree 1). So it is a collection of cycles.

    # Similarly for blue.

    # In such a graph, to route all the red balls to the X-1 box, we must be able to "collect" all the red balls by moving them along the edges until they reach X-1.

    # But note: the operation is defined as: when we operate on a box i, we remove the red from i and send it to P[i]. Then, if we want to move that red from P[i] to P[P[i]], we must operate on P[i] (which might have other red from other boxes as well).

    # However, we can think of the problem as: we need to "collect" all the red balls (from every box) into the X-1 box. The graph structure (cycles) will determine the minimum number of operations.

    # But note: the operation is defined per box and we can choose the order arbitrarily. However, we cannot change the graph structure.

    # Actually, we can consider the reverse: to get a red ball from a box i to the X-1 box, we need to follow the chain: i -> P[i] -> P[P[i]] -> ... until we reach X-1.

    # However, the operation does not require that we move one ball at a time. We move all the red from a box at once.

    # The key observation: the graph for red is a permutation, so it is a set of cycles. Similarly for blue.

    # For the red balls: we need to collect all the red balls (from all boxes) into the X-1 box. This is possible if and only if the X-1 box is in the same cycle as every other box? Actually, no: because we can move from a box i to P[i] and then from P[i] to P[P[i]], etc. So the entire graph is a permutation, and the connectivity is by cycles.

    # Actually, we can break down the graph for red: the graph is a permutation, so it is a set of cycles. Then, to collect all red balls into the X-1 box, we must have that the X-1 box is in a cycle that includes every box that has at least one red ball? Actually, no: we can move red balls from a box i to P[i] and then from P[i] to P[P[i]], etc. But note: we can also operate on a box multiple times. However, once we move a red ball from a box, that box becomes empty (for red). Then, to move red from a box, we must have received red from other boxes? Actually, no: the operation on a box i removes the red from i and sends it to P[i]. Then, if we want