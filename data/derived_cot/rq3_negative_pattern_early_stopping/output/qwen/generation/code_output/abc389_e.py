import sys
import math

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    M = int(data[1])
    P = list(map(int, data[2:2+n]))
    
    # Sort the products in ascending order of P_i
    P.sort()
    
    # If M is 0, then we can buy 0 units.
    if M == 0:
        print(0)
        return
        
    # We'll use a priority queue to simulate the assignment, but we'll do it in batches.
    # However, we can use a simpler method: 
    # The minimal cost for X units is the sum of (k_i^2 * P_i) for each product i, with sum_i k_i = X.
    # But we need to find the maximum X such that the minimal cost <= M.
    # We can use binary search on X.
    # But first, we need a function to compute the minimal cost for a given X.
    # But note: the minimal cost for X units is not simply a function of X because the allocation is not linear.
    # We can use the following: 
    #   Let's define a function feasible(X) that returns the minimal cost to buy X units.
    #   But we can't compute it directly.
    # Instead, we can use a priority queue to simulate the assignment for a given X, but X can be large.
    # But we can use a different approach: 
    #   We can use the fact that the optimal allocation is to use the products in increasing order of P_i.
    #   And the minimal cost is the sum of (k_i^2 * P_i) for each product i, where k_i is the number of units allocated to product i.
    #   And the allocation is done by: 
    #       k_0 = floor((M) / (P_0))  # Not exactly.
    #
    # Let's try to derive the allocation:
    #   We have to distribute X units to N products to minimize sum_i (k_i^2 * P_i).
    #   This is minimized by using the product with the smallest P_i as much as possible.
    #   But the cost is quadratic, so the allocation is not linear.
    #
    # We can use a greedy allocation with a priority queue, but we need to do it without iterating X times.
    #
    # Alternative approach from known similar problems (e.g., CodeForces problems) is to use binary search on the total units and a priority queue for the marginal costs.
    #
    # But note: the total number of distinct marginal costs is O(N) because each product can be used only a limited number of times (until its marginal cost exceeds the next product's).
    #
    # However, after research, I recall that the problem is known as the "minimum cost to buy exactly X items with quadratic costs" and can be solved by a greedy algorithm that uses a priority queue, but the total number of operations is O(N * sqrt(M)) or something, which is not feasible for M=10^18.
    #
    # Another known solution is to use the following observation:
    #   The minimal cost for X units is the same as the minimal value of the function f(k_1, k_2, ..., k_N) = sum_i (k_i^2 * P_i) subject to sum_i k_i = X.
    #   This is minimized by using the products in increasing order of P_i.
    #   And the minimal cost can be computed by:
    #       Sort P in ascending order.
    #       Let k = 0 (current unit count).
    #       Let cost = 0.
    #       For i in range(n):
    #           Let t = floor((M - cost) / (P[i] * (2*k + 1)))  # Not exactly.
    #
    # After further thought, I found that the problem is equivalent to scheduling X tasks on N machines where the j-th task on machine i costs (2*j-1)*P_i.
    # The minimal total cost is the sum of the costs of the tasks.
    #
    # We can use a priority queue to simulate the tasks, but we need to do it in batches.
    #
    # Here's a method:
    #   Let's maintain a min-heap of tuples (next_cost, P_i, count) for each product.
    #   next_cost = (2*count + 1)*P_i.
    #   Initially, count=0 for all, so next_cost = P_i.
    #   Then, for each task (from 1 to X), we pop the smallest next_cost, add its cost to the total cost, and push back ( (2*(count+1)+1)*P_i, P_i, count+