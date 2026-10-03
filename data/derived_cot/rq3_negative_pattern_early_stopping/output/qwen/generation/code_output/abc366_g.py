import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        print("No")
        return
    n = int(data[0])
    m = int(data[1])
    edges = []
    index = 2
    for i in range(m):
        u = int(data[index]); v = int(data[index+1]); index += 2
        edges.append((u-1, v-1))
    
    # If there are no edges, then we can assign any number (like 1) to each vertex.
    if m == 0:
        print("Yes")
        arr = [1] * n
        print(" ".join(map(str, arr)))
        return

    # Build the graph and the equations.
    # We'll represent the graph as an adjacency list.
    graph = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    # We are going to try to find a solution. The idea is to use the following:
    # For each vertex, the condition is: XOR of neighbors = 0.
    # This is equivalent to: for each vertex, the value at the vertex is determined by its neighbors? Not exactly.
    # Actually, the condition is a system of equations. But note: the condition for vertex i is:
    #   x_{i1} XOR x_{i2} XOR ... XOR x_{ik} = 0, where i1, i2, ..., ik are neighbors of i.
    #
    # However, note that the condition does not involve the value at the vertex itself. So we have a system of equations that are linear over GF(2) but with 60 bits per variable.
    #
    # But wait, the problem constraints say that the numbers are between 1 and 2^60-1, so they are non-zero and 60 bits. However, the equations are linear and homogeneous. The solution space is a vector space. We are to find if there exists a non-zero solution (but note: the numbers must be at least 1, so we cannot use 0). However, the homogeneous system might have the zero solution, but we need to assign non-zero numbers. But note: the problem does not require the numbers to be distinct, only between 1 and 2^60-1.
    #
    # Actually, the problem is asking: does there exist an assignment (each vertex gets a number in [1, 2^60-1]) such that for every vertex, the XOR of its neighbors is 0.
    #
    # Let me reframe: Let x_i be the number at vertex i. Then for each vertex i, we have:
    #   sum_{j in adj(i)} x_j = 0   (in GF(2)^60, component-wise)
    #
    # This is a system of linear equations over GF(2) with 60*N variables and N equations (one per vertex). But note: the equations are not independent. In fact, if we consider the entire graph, the sum of all equations (over GF(2)) would be:
    #   For each vertex i, we have the XOR of its neighbors. Then the total sum is: for each edge (u, v), the vertex v appears in the equation for u, and u appears in the equation for v. So each edge contributes twice, and the total sum is 0. So the system is consistent only if the graph is bipartite? Or maybe not.
    #
    # Actually, the system is:
    #   For each vertex i: sum_{j in adj(i)} x_j = 0
    #
    # This is a linear system. The solution space is the null space of the incidence matrix (over GF(2)) but with 60 bits per variable. However, we can break each x_i into 60 bits. Then the system becomes 60 * N equations (each bit of the condition must be 0) and 60 * N variables. But that is too heavy.
    #
    # Alternatively, note that the condition for each vertex is that the sum (XOR) of its neighbors is 0. This is similar to the condition for a linear system where the value at a vertex is determined by its neighbors. But actually, the condition is that the neighbors' values must XOR to 0. This is a constraint on the neighbors, not on the vertex itself.
    #
    # Another idea: consider the entire graph. The condition is that for each vertex, the XOR of its neighbors is 0. This is equivalent to saying that the graph is such that the assignment is a "closed" set under XOR for each vertex's neighborhood.
    #
    # Let me try to solve for a small graph. For example,