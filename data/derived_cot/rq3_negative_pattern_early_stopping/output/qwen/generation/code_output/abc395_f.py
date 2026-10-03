import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    x = int(data[1])
    pairs = []
    index = 2
    for i in range(n):
        u = int(data[index]); d = int(data[index+1]); index += 2
        pairs.append((u, d))
    
    # Calculate the total sum of all U_i + D_i
    total_sum = sum(u + d for u, d in pairs)
    # The maximum H we can choose is the minimum of all U_i + D_i
    min_sum = min(u + d for u, d in pairs)
    # But note: H must be at least 2, but min_sum might be 2 or more.

    # We are going to use dynamic programming to find the minimum total reduction.
    # However, note: the total reduction is total_sum - n * H, so we want to maximize H (to minimize reduction) but subject to the condition that we can form a smooth sequence of u_i's.

    # Alternatively, we can think: we want to choose H (from 2 to min_sum) and then check if there exists a sequence of u_i's (each u_i in [max(1, H-D_i), min(U_i, H-1)]) such that |u_i - u_{i+1}| <= X.

    # But note: the total reduction is fixed for a given H. So we want the maximum H (to minimize the total reduction) for which there exists a smooth sequence.

    # However, the condition for the sequence is non-linear and the range of H is from 2 to min_sum (which can be up to 2e9) so we cannot iterate over H.

    # We need to reframe the problem.

    # Observation: The condition for the upper teeth is that the sequence u_1, u_2, ..., u_N must be such that |u_i - u_{i+1}| <= X. This is a typical condition for a sequence with bounded differences.

    # Also, for each i, u_i must be in [L_i, R_i] where L_i = max(1, H - D_i) and R_i = min(U_i, H-1).

    # We want to know if there exists a sequence u_1, u_2, ..., u_N such that for each i, L_i <= u_i <= R_i and |u_i - u_{i+1}| <= X.

    # This is a classic problem that can be solved by dynamic programming with state i (the tooth index) and the value of u_i. But the range of u_i can be very large (up to 10^9) so we cannot iterate over all values.

    # We can use a segment tree or a Fenwick tree? Or we can use a different approach.

    # Alternatively, we can use a greedy method or binary search on H? But note: the total reduction is fixed for a given H, so we want the maximum H for which the sequence exists.

    # But note: the condition for the sequence depends on H. So we need to check for a given H if there exists a sequence. How?

    # We can use a two-pointer or a sliding window to check connectivity between the intervals [L_i, R_i] with the constraint that consecutive values differ by at most X.

    # Actually, we can use a graph where each node i has an interval [L_i, R_i] and edges between i and i+1 require that the two intervals overlap by at least X? Actually, the condition is that there exists a value in [L_i, R_i] and [L_{i+1}, R_{i+1}] such that |a - b| <= X.

    # This is equivalent to: the intervals [L_i, R_i] and [L_{i+1}, R_{i+1}] must have a non-empty intersection in the graph of allowed values with edges of length X.

    # But note: the condition is not about the intervals overlapping, but about the existence of two numbers a and b (from the two intervals) such that |a - b| <= X.

    # This is equivalent to: the intervals [L_i, R_i] and [L_{i+1}, R_{i+1}] must have a gap of at most X between them? Actually, no. The condition is that the two intervals must be "close" in the sense that the distance between the two intervals is at most X.

    # Actually, the condition for two consecutive teeth i and i+1 is that there exists a in [L_i, R_i] and b in [L_{i+1}, R_{i+1]] such that |a - b| <= X.

    # This is equivalent to: the