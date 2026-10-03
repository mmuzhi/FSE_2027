import sys
from collections import deque

def main():
    data = sys.stdin.read().splitlines()
    if not data:
        return
    n = int(data[0])
    graph = []
    for i in range(1, n+1):
        line = data[i].strip()
        graph.append(line)
    
    # Build the actual graph structure: graph[i][j] is the edge from i to j (0-indexed)
    # We'll create a list of lists for the graph, but we can also keep the input as is.
    # We'll create a 2D list for the graph: graph[i][j] is the character or '-' for no edge.
    # But we need to know the edges. We can build a directed adjacency list: for each vertex i, list of (neighbor, label)
    adj = [[] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            ch = graph[i][j]
            if ch != '-':
                adj[i].append((j, ch))
    
    # We'll use BFS in a state space: (current_vertex, current_string) but that's too heavy because string can be long.

    # Alternatively, we can use a different idea: 
    # We are to find the shortest path (in terms of number of edges) such that the concatenated labels form a palindrome.
    # We can consider that the entire path's label string is a palindrome. Let the path have k edges. Then the first ceil(k/2) edges must match the reverse of the last ceil(k/2) edges.

    # But note: we can also use the fact that the path is from i to j. We can consider the path as two parts: the forward part and the backward part, but the graph is directed.

    # Another idea: use two BFS runs? Or use a state (v, w) where w is the current "half" of the palindrome that we have built so far, but we are building from both ends? 

    # Actually, we can use a state (v, w) where w is the current string that we have built so far (the entire path's label string). But the string can be long and the state space is too big.

    # We need a smarter way.

    # Observation: The palindrome condition is that the entire string is symmetric. We can break the path into two parts: the forward part and the backward part. But note, the path is from i to j, so the entire path is fixed.

    # Alternatively, we can use the concept of "palindromic paths" by considering the reverse graph and matching the labels.

    # Let me think: 
    # We want a path from i to j: i = v0 -> v1 -> ... -> vk = j, and the labels are l0, l1, ..., l_{k-1}. Then the string is s = l0 l1 ... l_{k-1}. We require s == reverse(s).

    # We can also consider that the path is built by matching the first and last edges, then the second and second last, etc.

    # We can use a BFS that goes from i to j, but we need to remember the entire string? That's too heavy.

    # Another idea: use a state (v, l, r) where l and r are the current positions in the string? But that's not helpful.

    # Wait, but note: the problem is asking for the shortest path. So we can use BFS by the number of edges. But the state must include the current vertex and the "memory" of the string that has been built so far. However, the string can be long, but the minimal length is what we are after, and we are only interested in the minimal length.

    # But the state space is too big because the string can be arbitrary.

    # Alternatively, we can use a state (v, w) where w is the current "pending" part that must be matched by the future. But the pending part is the part that we have built so far and must be matched by the reverse. However, the entire path is built from i to j, so we are building the string from the beginning. 

    # Actually, we can use a state (v, w) where w is the current string (the entire path so far). But the string can be up to 100 characters (since N=100, and each edge one character, so maximum 100 edges). But 100^100 states is too many.

    # We need to find a better way.

    # Let me consider the following: 
    # We are allowed to use cycles. The minimal path might be found by going through cycles to build a palindrome.

    # Another idea: use a two-dimensional array dp[i][j] for the minimal