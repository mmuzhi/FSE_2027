import sys

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    
    n = int(data[0])
    points_p = []
    index = 1
    for i in range(n):
        a = int(data[index]); b = int(data[index+1]); index += 2
        points_p.append((a, b))
    points_q = []
    for i in range(n):
        c = int(data[index]); d = int(data[index+1]); index += 2
        points_q.append((c, d))
    
    # We'll try to find a permutation R (0-indexed) such that the segments do not cross.
    # One known approach is to use a greedy matching with a stack or by sorting both sets and then matching in a specific order.

    # Sort both sets by x-coordinate (and if same x, by y-coordinate)
    points_p_sorted = sorted(points_p, key=lambda x: (x[0], x[1]))
    points_q_sorted = sorted(points_q, key=lambda x: (x[0], x[1]))
    
    # Now, we can try to match the leftmost P to the leftmost Q, then the next P to the next Q, etc., but that might not work because the segments might cross.

    # Alternatively, we can use a recursive backtracking with pruning, but N can be up to 300, so that's too slow.

    # Another idea: use a greedy matching by considering the convex hull or by using the fact that the matching must be non-crossing.

    # Actually, there's a known algorithm: 
    # 1. Sort the P points by x-coordinate.
    # 2. For each P point, consider the Q points in increasing x-order and choose the one that is not taken and that is to the right of the previous Q's? 

    # But wait, the non-crossing condition is more about the order of the endpoints.

    # Another known method: 
    #   - Sort the P points by x-coordinate.
    #   - Sort the Q points by x-coordinate.
    #   - Then, we can use a greedy algorithm that for each P point (from left to right), we choose the Q point (from left to right) that is not taken and that is to the right of the previous Q's? 

    # Actually, the standard non-crossing bipartite matching is to use the following: 
    #   - Sort both sets by x-coordinate.
    #   - Then, the matching is non-crossing if and only if the matching is "monotone" in the sense that the Q points are matched in increasing x-order.

    # But that's not sufficient. 

    # Alternatively, we can use the following: 
    #   - For each P_i, we can determine the set of Q_j that are "visible" (i.e., not blocked by other points) but that's complex.

    # After some thought, I recall that one way to solve this is to use a bipartite graph and then use a matching algorithm that enforces non-crossing. But how to define the edges?

    # Actually, we can define an edge between P_i and Q_j only if the segment (P_i, Q_j) does not cross any other segment that we might assign. But that's too vague.

    # Another idea: use a greedy algorithm that for each P_i (sorted by x), we choose the Q_j (sorted by x) that is the closest in x-coordinate and not taken, but that might not work.

    # Wait, there's a known problem: "Matching on a line" or "non-crossing matching" in two sets. 

    # Standard solution: 
    #   - Sort the P points by x-coordinate.
    #   - Sort the Q points by x-coordinate.
    #   - Then, the matching is non-crossing if we match the i-th P to the i-th Q in the sorted order? Not necessarily.

    # But wait, if we sort both by x, then the segments might cross if the order of Q is not the same as the order of P. 

    # Actually, the non-crossing condition is equivalent to: the permutation R must be such that the sequence of Q points (in the order of increasing x-coordinate) is the same as the sequence of P points (in increasing x-coordinate) but possibly with a different order? 

    # No, that's not true.

    # After some research in my mind, I recall that one way to solve this is to use a recursive function that tries to assign the leftmost P to a Q that is not taken and then recursively solves the left and right parts. But that's exponential.

    # Alternatively, we can use a greedy matching by considering the entire set of points and using the fact that the matching must be