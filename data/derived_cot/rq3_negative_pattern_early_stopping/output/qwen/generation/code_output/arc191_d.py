import sys
from collections import deque

def main():
    data = sys.stdin.read().split()
    it = iter(data)
    n = int(next(it)); m = int(next(it)); s = int(next(it)); t = int(next(it))
    graph = [[] for _ in range(n+1)]
    for _ in range(m):
        u = int(next(it)); v = int(next(it))
        graph[u].append(v)
        graph[v].append(u)
    
    # We'll compute the shortest path from S to T and from T to S (same) and also from S to S (for B) and T to T (for A) but wait, no.

    # Actually, we need to compute the shortest path from S to T (for A) and from T to S (for B). But also, we need to consider that the two pieces might take different paths.

    # However, note that the minimal number of moves is the sum of the two distances if we can avoid collisions. But sometimes we cannot use the direct path because of the constraint.

    # But wait, the problem is symmetric. The minimal number of moves is the minimal k such that there exists two paths (one for A from S to T and one for B from T to S) and the two paths do not share any vertex at the same time. But the state space is too big.

    # Another idea: consider that the two pieces must swap. The minimal number of moves is the minimal k such that there exists a sequence of k moves (each move is one piece moving one step) and the two pieces end up swapped.

    # We can use a BFS that considers the state (a, b) but that's too expensive.

    # Alternatively, we can use a two-layered graph or consider the following:

    # Let d1 = shortest distance from S to T (for A)
    # Let d2 = shortest distance from T to S (for B) — same as d1.

    # But the direct move is blocked because if we move A from S to T in d1 steps, then during the move, B is at T and we cannot have A and B on the same vertex. Similarly, if we move B from T to S, then during the move, A is at S and we cannot have B and A on the same vertex.

    # So we need to use longer paths.

    # Actually, the problem is similar to the "two ants" problem. 

    # We can consider that the two pieces must each travel from their start to the target. The minimal total moves is the sum of the two distances, but we must avoid having them on the same vertex at the same time.

    # But note, we can interleave the moves. So the two pieces can move independently, but their positions must never coincide.

    # We can model this as a graph where each node is (a, b) and edges are moving one piece to an adjacent vertex (if the new state is not (a, b) with a==b). But the state space is too big.

    # We need to find a better way.

    # Observation: the goal is to swap the two pieces. The minimal number of moves must be at least the distance from S to T (for A) and the distance from T to S (for B). But because of the constraint, we might need to take detours.

    # Another idea: consider the graph and the two pieces. The minimal number of moves is the minimal k such that there exists a path for A from S to T of length k1 and a path for B from T to S of length k2, and the two paths (the sequences of vertices) do not have any vertex in common at the same time step. But the time steps are interleaved arbitrarily.

    # Actually, the problem is equivalent to: we have two tokens, and we want to swap them. The minimal number of moves is the minimal k such that there exists two paths (for A and B) that are vertex-disjoint at every step (but the steps are interleaved, so the two paths can share vertices as long as they are not at the same step). 

    # But note, the graph is static. We can precompute the shortest path from S to T and from T to S (which are the same). 

    # However, the minimal number of moves might be the sum of the two distances if the two paths do not conflict. But if they do, we need to find alternative paths.

    # Alternatively, we can consider that the two pieces must meet the condition by having one piece move away from the target so that the other can enter. 

    # Let me define:
    # Let d1 = shortest distance from S to T (for A)
    # Let d2 = shortest distance from T to S (for B)

    # But the direct move is blocked. So we need to use a