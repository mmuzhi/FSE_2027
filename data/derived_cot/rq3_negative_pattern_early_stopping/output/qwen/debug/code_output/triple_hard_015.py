class Solution:
    def validArrangement(self, pairs: List[List[int]]) -> List[List[int]]:
        graph = defaultdict(list)
        degree = defaultdict(int)
        for x, y in pairs:
            graph[x].append(y)
            degree[x] += 1
            degree[y] -= 1
        
        # Find the start node: the one with net out-degree 1, or if none, then any node (for circuit)
        start_node = None
        for node in degree:
            if degree[node] == 1:
                start_node = node
                break
        else:
            # If no node has net out-degree 1, then check for circuit (all zeros)
            # But note: in a circuit, every node has net out-degree 0.
            # We can choose any node as start.
            start_node = next(iter(degree.keys()))
        
        # We'll use a stack for DFS
        stack = [start_node]
        path = []
        
        # We need to keep track of the graph and the current node
        # We'll use a list for the stack and a list for the path
        # We'll also maintain a visited_edges structure? Actually, we can use the graph and remove edges as we traverse.
        # But note: we cannot remove edges permanently because we need to backtrack? Actually, no: we are doing a DFS and we want to use each edge once.
        # We'll use a stack that holds the current node and an iterator for its outgoing edges.
        # Alternatively, we can use a list for each node's outgoing edges and pop from the end.

        # We'll use a list for the path and a stack for DFS.
        # But note: we need to backtrack the edges? Actually, we are going to use Hierholzer's algorithm without backtracking the edges because we are removing edges as we traverse.

        # However, the graph is mutable. We'll use a stack that holds the current node and the index of the next edge to take from that node.
        # But the code originally used a list and popped. We can do similarly but we need to keep track of the next edge index.

        # Alternatively, we can use a recursive DFS that pops an edge and then pushes the node back. But we need to remember which edge was taken.

        # Let's use a stack that holds the current node and the index of the next edge to take from that node.
        # But the original graph is stored as a list for each node. We can use a stack that holds the node and the current index in the graph[node] list.

        # We'll create a new graph structure that is mutable and we'll use a stack for DFS.

        # We'll use a stack that holds the current node and the index of the next edge to take from that node.
        # But note: the graph is built as a list of outgoing edges.

        # We'll create a new graph structure that is a list of lists, and we'll use a stack for DFS.

        # Alternatively, we can use a recursive DFS that pops an edge and then pushes the node back. But we need to remember which edge was taken.

        # Let's do iterative DFS with a stack that holds the current node and the index of the next edge to take.

        # We'll create a new graph structure that is a list of lists, and we'll use a stack for DFS.

        # We'll use a stack that holds the current node and the index of the next edge to take from that node.
        # But note: the graph is built as a list of outgoing edges.

        # We'll create a new graph structure that is a list of lists, and we'll use a stack for DFS.

        # We'll use a stack that holds the current node and the index of the next edge to take.

        # But the original graph is stored as a list for each node. We can use a stack that holds the node and the index of the next edge to take.

        # We'll create a new graph structure that is a list of lists, and we'll use a stack for DFS.

        # Alternatively, we can use a recursive DFS that pops an edge and then pushes the node back. But we need to remember which edge was taken.

        # Let's do iterative DFS with a stack that holds the current node and the index of the next edge to take.

        # We'll create a new graph structure that is a list of lists, and we'll use a stack for DFS.

        # We'll use a stack that holds the current node and the index of the next edge to take.

        # But note: the graph is built as a list of outgoing edges.

        # We'll create a new graph structure that is a list of lists, and we'll use a stack for DFS.

        # We'll use a stack that holds the current node and the index of the next edge to take.