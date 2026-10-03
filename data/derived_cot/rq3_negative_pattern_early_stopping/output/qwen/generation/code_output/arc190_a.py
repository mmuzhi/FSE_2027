import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        print(-1)
        return
    
    n = int(data[0])
    m = int(data[1])
    intervals = []
    for i in range(m):
        l = int(data[2+2*i])
        r = int(data[3+2*i])
        intervals.append((l, r))
    
    # We are going to use a greedy approach: we want to cover the entire range [1, n] with the minimum number of operations (each operation can be either an interval or its complement).

    # However, note that operation 2 (complement) is expensive because it covers two intervals (the left part and the right part). But we can think of the problem as: we have two types of intervals: the given intervals (operation 1) and their complements (operation 2). But note: the same operation can be used as either operation 1 or operation 2.

    # Alternatively, we can think of the problem as: we need to cover the entire [1, n] with intervals (each operation can contribute either the given interval or the complement). But note: the complement of [L, R] is [1, L-1] ∪ [R+1, n]. So we have two intervals per operation.

    # But note: the operations are independent and we can choose for each operation which one to use. We want to cover [1, n] with the minimum number of intervals (each interval is either the given one or its complement) and we can use each operation only once.

    # This is a hitting set problem? Or set cover? But set cover is NP-hard, but note that M can be up to 200000 and N up to 1000000. We need a better approach.

    # Another perspective: consider that each operation can be represented as a set of indices it covers. Operation 1 covers [L_i, R_i], operation 2 covers [1, L_i-1] ∪ [R_i+1, n]. We want to choose a subset of operations (each operation can be used in one of the two ways) such that the union of the chosen sets is [1, n] and the number of operations chosen is minimized.

    # But note: we are allowed to use operation 0 (skip) for any operation, so we can choose which operations to use and for each used operation, choose one of two sets.

    # This is a variant of the interval cover problem, but with two types of intervals per operation.

    # Let me think of a different approach: we can consider that the entire sequence must be covered. We can use a greedy interval covering technique.

    # But note: operation 2 (complement) is tricky because it covers two intervals. However, we can reframe the problem: we need to cover [1, n]. Each operation i can be used to cover either A_i = [L_i, R_i] or B_i = [1, L_i-1] ∪ [R_i+1, n]. We want to choose a set of operations (and for each, choose A_i or B_i) such that the union is [1, n] and the number of operations is minimized.

    # This is similar to the classic "interval covering" but with two types of intervals.

    # Alternatively, we can think of the problem as: we have two types of intervals (forward and backward) and we want to cover the entire range. But note: the complement intervals are not contiguous.

    # Another idea: consider that the entire range [1, n] must be covered. We can use a greedy algorithm that processes the operations in a particular order. But note: the operations are given in a fixed order, but the order of operations doesn't matter because the operations are independent (they just set 1s and don't unset). So we can reorder the operations arbitrarily.

    # But wait: the problem says "In the i-th operation, you are given an integer pair (L_i, R_i)" and we must output the operations in the given order. However, the operations are independent, so the order of operations doesn't affect the final state. So we can choose for each operation independently.

    # So the problem reduces to: from M operations, each operation i can contribute either A_i or B_i (or nothing). We want to cover [1, n] with the minimum number of operations (each operation can be used at most once, and we can choose which set to use).

    # This is a hitting set problem where the universe is [1, n] and each operation i gives two sets A_i and B_i. We want to choose a subset of operations and for each operation, choose one of the two sets, such that the union of the chosen sets