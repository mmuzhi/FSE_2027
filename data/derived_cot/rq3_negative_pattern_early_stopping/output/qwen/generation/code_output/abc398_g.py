import sys
from collections import deque, defaultdict

def main():
    data = sys.stdin.read().split()
    it = iter(data)
    n = int(next(it)); m = int(next(it))
    graph = [[] for _ in range(n+1)]
    edges = []
    for _ in range(m):
        u = int(next(it)); v = int(next(it))
        graph[u].append(v)
        graph[v].append(u)
        edges.append((u, v))
    
    # We'll do a BFS/DFS to color the graph (bipartite check)
    color = [-1] * (n+1)
    color[1] = 0
    q = deque([1])
    while q:
        node = q.popleft()
        for neighbor in graph[node]:
            if color[neighbor] == -1:
                color[neighbor] = color[node] ^ 1
                q.append(neighbor)
            else:
                if color[neighbor] == color[node]:
                    # This should not happen if the graph is bipartite, but given the constraint, we assume it is.
                    pass

    # Now, we need to count the number of edges that can be added without creating an odd cycle.
    # But note: the game is about adding edges that do not create an odd cycle. In a bipartite graph, an edge can be added only between two vertices of different colors (in the same connected component) or between two vertices from different components (and then we can flip the colors of one component to make it bipartite). However, the condition is that the graph must not have an odd cycle. So, the edge must be between two vertices of different colors (after possibly flipping one component's colors).

    # But note: the entire graph is bipartite, so we can assign two colors (0 and 1) to all vertices. However, the bipartition is fixed per connected component. But when adding an edge between two components, we can flip the colors of one component arbitrarily. Therefore, the only restriction is that the edge must not be between two vertices of the same color in the fixed bipartition of the entire graph? Actually, no. Because we can flip one component's colors. So, for two vertices from different components, we can always choose the color of one component so that the edge is between two different colors. Therefore, edges between different components can always be added without creating an odd cycle.

    # But wait, what about edges within the same component? In the same component, the bipartition is fixed. So, an edge between two vertices of the same color in the same component would create an odd cycle. But an edge between two vertices of different colors in the same component is already present or not? Actually, the graph is simple, so we don't have multiple edges. But the condition is that the edge must not already exist.

    # Therefore, the moves are:
    # 1. Adding an edge within the same component between two vertices of different colors (if not present) is allowed. But wait, in a bipartite graph, edges are only between different colors, so such edges are the existing edges. But the graph is simple, so we cannot add an existing edge. So, within a component, we can only add edges between vertices of the same color? No, because that would create an odd cycle. So, within a component, we cannot add any edge because the bipartition is fixed and edges between same color are forbidden.

    # Actually, no. The graph is bipartite, so edges are only between different colors. So, the existing edges are between different colors. The missing edges in the same component are between same colors. And adding an edge between same colors in the same component would create an odd cycle. So, we cannot add any edge within the same component.

    # Now, what about edges between different components? We can add them because we can flip the colors of one component to make the edge connect different colors. So, the entire graph remains bipartite.

    # Therefore, the game is about connecting different connected components. Each move must connect two different components (because within a component, no edge can be added without creating an odd cycle). And the graph starts with M edges and N vertices, so the number of connected components is comp = n - m + (cycles) but actually, we can compute the number of connected components.

    # Actually, the graph is given with M edges and N vertices. The number of connected components is the number of bipartite parts we found? No, the BFS/DFS we did was from vertex 1, but the graph might be disconnected. So, we need to count the connected components.

    # Let me modify the BFS to count connected components.

    visited = [False] * (n+1)
    components = []
    color = [-1] * (n+1)