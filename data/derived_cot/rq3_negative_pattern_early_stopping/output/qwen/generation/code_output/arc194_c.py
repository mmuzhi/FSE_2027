import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1+n]))
    B = list(map(int, data[1+n:1+2*n]))
    C = list(map(int, data[1+2*n:1+3*n]))
    
    # Identify the indices where A_i != B_i
    diff = [i for i in range(n) if A[i] != B[i]]
    
    # We need to flip each index in diff an odd number of times, and the others even (could be zero).
    # The minimal total flips is |diff|, but we can also flip more (even times) to adjust the cost.

    # However, note: the cost of an operation is the entire array's current value (A) dotted with C.

    # Let x_i be the number of times we flip index i. Then the condition is: x_i % 2 == 1 for i in diff, and x_i % 2 == 0 for others.

    # The total cost is the sum over operations (each operation is a flip) of the current A vector's dot product with C.

    # But note: the state of the array changes with each operation.

    # We can also think: the entire process is a sequence of operations. Each operation flips one index and then the cost is the entire array's current value.

    # Let's denote by y_i the state of index i at the beginning (initial A_i). Then, after a sequence of operations, the state of index i is y_i xor (number of flips at i mod 2).

    # The cost of the k-th operation is the entire array's state at that time (a vector of 0/1) dotted with C.

    # We can also note that the entire process can be broken down by the order of flips. However, the problem is complex.

    # Another idea: consider that the minimal total cost is achieved by flipping the indices in diff, but we can also flip some indices multiple times (even) to "postpone" the cost or to use cheaper flips.

    # Actually, note: flipping an index that is not in diff an even number of times doesn't change the state and doesn't help the condition, but it might be used to adjust the cost? 

    # But the condition requires that the final state is B. So we must flip each index in diff an odd number of times and the others an even number of times.

    # The minimal total flips is |diff|, but we can also flip an index in diff more than once (say, 3 times) and then we have to account for the extra cost.

    # However, the cost is not linear in the number of flips. The cost of an operation is the entire array's current value at the time.

    # We can also consider that the entire process is a sequence of operations. The state of the array is a vector of 0/1. The goal is to go from A to B.

    # We can model the problem as a graph where each node is a state (a vector of n bits) and edges are flips (each edge has a cost that is the entire array's dot product with C at the time of the edge). But n can be up to 200,000, so we cannot do that.

    # We need a smarter way.

    # Observation: The cost of an operation is the sum_{i} (current_A_i * C_i). Notice that the cost is the same as the dot product of the current A and C.

    # Also note: the effect of flipping an index i is to change A_i (from 0 to 1 or 1 to 0). 

    # Let's define:
    #   Let x_i be the total number of flips at index i (so the final state of index i is A_i xor (x_i % 2)).

    # The condition: for each i, (A_i xor (x_i % 2)) == B_i.

    # The total cost is the sum_{operations} (current_A · C).

    # But note: the current_A during the operations is the initial A with some flips applied. 

    # We can also note that the entire process can be broken down by the order of flips. However, we can also consider the following:

    # Let F be the set of indices that are flipped an odd number of times (so F must be exactly the set of indices where A_i != B_i). Then, the minimal total flips is |F|.

    # But the cost is not just |F| * (some base cost) because the cost of each operation depends on the entire array.

    # However, note: the cost of an operation is the entire array's current value. We can also consider