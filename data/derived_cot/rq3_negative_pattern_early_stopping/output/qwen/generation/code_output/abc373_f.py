import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    
    n = int(data[0])
    W = int(data[1])
    items = []
    index = 2
    for i in range(n):
        w = int(data[index]); v = int(data[index+1]); index += 2
        items.append((w, v))
    
    # We'll use dynamic programming. The state is the total weight so far, and we want to maximize the total happiness.
    # But note: the happiness for each type is quadratic. However, we can precompute for each type the best happiness for a given weight?
    # Alternatively, we can use a two-dimensional DP: dp[i][w] = maximum total happiness achievable with the first i types and total weight w.
    # But the state space is (n+1) * (W+1) which is 3000*3000 = 9e6, which is acceptable.

    # However, for each type, we can choose multiple items (but the number is limited by the weight). But note: the happiness function for a type is concave, so the optimal number of items for a type is limited. But we can't precompute all k for each type because k can be up to W (3000) and then the state space would be 3000*3000*3000 which is 27e9, too big.

    # We need to use a different approach. We can use a knapsack that considers each type and the number of items chosen from that type. But the number of items per type is too high.

    # Alternatively, we can use a state that is the total weight and then for each type, we try all possible k (from 0 to floor(W/w_i)) but that is too many.

    # Another idea: the happiness function for a type is separable and concave. We can use a greedy or a convex hull trick? Or note that the problem is similar to the quadratic knapsack.

    # Let me think: the total happiness is sum_i (k_i * v_i) - sum_i (k_i^2). We can also write it as: sum_i (k_i * (v_i - k_i)).

    # But note: the problem is equivalent to: maximize sum_i (k_i * v_i) - sum_i (k_i^2) subject to sum_i (k_i * w_i) <= W and k_i >= 0, integer.

    # This is a quadratic optimization. We can use a two-step approach: first, for each type, the optimal k_i is the integer closest to v_i/2 (but we have to consider the weight constraint). But then, how to combine?

    # Alternatively, we can use a DP that iterates over types and for each type, we consider the weight used and the happiness. But the state space is too big.

    # Another idea: since the total weight is only 3000, the total number of items is at most 3000 (if each item has weight 1). So we can consider a DP that iterates over the total number of items (from 0 to 3000) and the types, but that is still 3000*3000=9e6 states, but then for each state, we need to know which items we chose, which is not feasible.

    # Alternatively, we can use a knapsack that for each type, we precompute the best happiness for a given weight, but the weight for a type can be chosen in multiples (but the happiness is quadratic). 

    # Let me define for each type i, the function f_i(x) = x * v_i - x^2, but only for x from 0 to floor(W/w_i). But W is 3000, so for each type, we can precompute an array of length (floor(W/w_i)+1) with the happiness for x items. Then, we can combine these functions with a knapsack. But the number of types is 3000, and the maximum x for each type is floor(W/w_i) which can be up to 3000, so the total state space is 3000 * 3000 * 3000 which is 27e9, which is too big.

    # We need a more efficient way.

    # Observation: the happiness function for each type is concave and quadratic. The optimal solution will not choose more than a few hundred items from a single type? Actually, the optimal k for a type is around v_i/2. But v_i can be up to 10^9, so k can be up