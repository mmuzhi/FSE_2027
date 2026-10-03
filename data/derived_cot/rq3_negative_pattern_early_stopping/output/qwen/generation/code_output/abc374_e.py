import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        print(0)
        return
    
    n = int(data[0])
    x = int(data[1])
    processes = []
    index = 2
    for i in range(n):
        A = int(data[index]); P = int(data[index+1]); B = int(data[index+2]); Q = int(data[index+3])
        index += 4
        processes.append((A, P, B, Q))
    
    # If no processes, then capacity is 0.
    if n == 0:
        print(0)
        return

    # We'll use binary search on M (the production capacity)
    # The lower bound can be 0, and the upper bound can be set by considering the maximum M we can get from one process and then the minimum over all processes.
    # But note: we can set M as high as the maximum of the minimums we can achieve by each process individually, but we must consider the budget.

    # However, note that the production capacity is the minimum of the outputs of all processes. So we cannot exceed the maximum M that the cheapest process can achieve.

    # Let's set an upper bound: for each process i, the maximum M we can achieve without budget constraint is unbounded, but with budget constraint, we can set an upper bound.

    # Alternatively, we can set an upper bound as the maximum M such that there exists a way to assign machines to each process to get at least M, and the total cost <= X.

    # But note: the minimal cost for a process i to achieve M is the minimum cost to cover M with two items (A_i, P_i) and (B_i, Q_i). We can compute the minimal cost for a fixed M for process i.

    # However, we cannot iterate M from 0 to a very high number (like 10^14) because of the budget constraint and the fact that M is the minimum over all processes.

    # Instead, we can use binary search on M. The idea:

    #   Let f(M) = total minimal cost to achieve at least M for every process (i.e., for each process i, we compute the minimal cost to get at least M, and then sum them up).

    #   Then, we want the maximum M such that f(M) <= X.

    # But note: the minimal cost for a process i to achieve at least M is computed by solving:

    #   minimize (x * P_i + y * Q_i) subject to x * A_i + y * B_i >= M, x, y nonnegative integers.

    # We can solve this by considering two cases:

    #   Case 1: Use only S_i machines. Then we need ceil(M / A_i) machines, so cost = ceil(M / A_i) * P_i.
    #   Case 2: Use only T_i machines. Then we need ceil(M / B_i) machines, so cost = ceil(M / B_i) * Q_i.
    #   Case 3: Use a combination.

    # But note: we can use a linear programming relaxation and then round up. However, we can use a greedy approach:

    #   We can use the following: Let y be the number of T_i machines. Then the remaining capacity needed is max(0, M - y * B_i). Then the number of S_i machines needed is ceil((M - y * B_i) / A_i) if M - y * B_i > 0, else 0.

    #   Then the cost is y * Q_i + ceil((M - y * B_i) / A_i) * P_i, but we must consider that if M - y * B_i <= 0, then we don't need S_i.

    #   We can iterate y from 0 to ceil(M / B_i) but M can be very large.

    # Alternatively, we can use a two-pointer or a mathematical formula. But note that we are going to use binary search on M, and for each M we need to compute the minimal cost for each process.

    # We need an efficient way to compute the minimal cost for a fixed M and process i.

    # We can use the following method for a fixed M and process (A, P, B, Q):

    #   Let f(M) = minimal cost for process i to achieve at least M.

    #   We can consider two cases: using only S_i or only T_i, but also combinations.

    #   We can use the idea: we want to minimize cost = x * P + y * Q, subject to x * A + y * B >= M.

    #   We can let y vary from 0 to ceil(M / B) (but note: we can also use more