import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    k = int(data[1])
    x = int(data[2])
    T = list(map(int, data[3:3+n]))
    
    # We'll use dynamic programming.
    # Let dp[i] be the minimum total dissatisfaction for the first i orders.
    # We need to consider the last shipment that covers some orders.
    # But the state must also remember the last shipment day? But T_i are large.

    # Alternatively, we can use a DP that considers the last shipment's start (the day we shipped the last group) and the index of the last order.

    # But note: the shipment day for a group is the day we ship it, which must be at least the maximum T_i in the group, and then the next shipment must be at least that day + X.

    # We can use a DP that iterates over orders and decides when to form a shipment.

    # Let dp[i] be the minimum total dissatisfaction for the first i orders, and we also keep track of the last shipment day (or the last day we shipped, which is the day of the last shipment). But the last shipment day can be very large (up to 10^12 + 10^9) so we cannot use it as state.

    # Instead, we can use a state that is the index i (the last order considered) and the last shipment day is determined by the last shipment we did. But we need to know the last shipment day to enforce the gap.

    # Alternatively, we can use a state that is the index i and the last shipment day is the day we shipped the last group (which is at least the maximum T_j for j in the last group). But we don't know the exact day, but we know that the next shipment must be at least last_shipment_day + X.

    # But note: the shipment day for a group must be at least the maximum T_i in the group. And we can choose to ship a group on any day as long as it is at least the maximum T_i and at least the previous shipment day + X (if there was a previous shipment).

    # We can use a DP that goes order by order and decides to form a shipment ending at the current order.

    # Let dp[i] = minimum total dissatisfaction for the first i orders, and we also keep track of the last shipment day (which is the day we shipped the last group). But the last shipment day is not stored in the state because it can be very large.

    # Instead, we can use a state that is the index i and the last shipment day is the day we shipped the last group. But we cannot store the day because it is too large.

    # Another idea: since the orders are given in increasing T_i, we can consider that the shipment day for a group is the maximum T_i in the group (if we ship immediately) or later (if we have to wait because of the gap). But we can always choose to ship a group on the maximum T_i of the group, unless the previous shipment day + X is greater than that.

    # Actually, the shipment day for a group must be at least max(T_j for j in the group) and at least (previous shipment day + X). So the actual shipment day is the maximum of these two.

    # But then the state must remember the previous shipment day. However, the previous shipment day is determined by the previous group's shipment day, which is the maximum of (max T_j in the previous group) and (previous previous shipment day + X). This seems recursive.

    # Alternatively, we can use a greedy grouping and then calculate the dissatisfaction.

    # But note: the problem is NP-hard in general? But N is only 100, so we can use exponential DP.

    # Let me define dp[i][j] where i is the number of orders processed and j is the number of orders in the last shipment (from 1 to k). But then we need to know the last shipment day to enforce the gap for the next shipment.

    # Alternatively, we can use a state that is the index i (the last order considered) and the last shipment day (the day we shipped the last group). But the last shipment day can be very large, but note that the only relevant last shipment days are the ones that are the maximum T_i of some group or the previous last shipment day + X. And the T_i are given, so the last shipment day is one of the T_i or T_i + multiples of X? Not exactly.

    # Another idea: since the orders are sorted by T_i, we can consider that the shipment day for a group is the maximum T_i in the group (if we don't have to wait) or the previous shipment day + X (if that is