class Solution:
    def validArrangement(self, pairs: List[List[int]]) -> List[List[int]]:
        graph = defaultdict(list)
        net_degree = defaultdict(int)
        for x, y in pairs:
            graph[x].append(y)
            net_degree[x] += 1
            net_degree[y] -= 1
        
        # Check Eulerian trail conditions
        start, end = None, None
        for node, degree in net_degree.items():
            if degree == 1:
                start = node
            elif degree == -1:
                end = node
        
        # If conditions not met, return empty list
        if start is None or end is None:
            return []
        
        # If the graph is empty, return empty list
        if not graph:
            return []
        
        # We'll use Hierholzer's algorithm
        stack = [start]
        result = []
        
        # We need to traverse until the stack is empty
        while stack:
            node = stack[-1]
            if graph[node]:
                next_node = graph[node].pop()
                stack.append(next_node)
                # Record the edge from node to next_node
                result.append([node, next_node])
            else:
                result.append([node, node])  # This is a dummy edge to mark the end of the trail for the last node?
                stack.pop()
        
        # Now, we have the trail in reverse order (from end to start) but we need to reverse it.
        # But note: the result list is built in the order of the trail from start to end? Actually, we are appending edges as we go, but the stack pops from the end.
        # Let me explain: 
        #   We start at 'start'. We push nodes until we can't. Then we pop and record the edge from the popped node to itself (dummy) and then the next edge is from the previous node.
        #   Actually, the result list is built in the order of the trail, but we are appending edges as we go. However, the last edge we append is the one that closes the trail? 
        #   But note: the condition of the Eulerian trail is that we start at 'start' and end at 'end'. The result list should be a list of edges [start, ... , end].
        #   However, the above code appends an edge [node, node] when popping, which is not part of the original graph. We should not do that.

        # Let's restructure: We don't need to record the dummy edge. Instead, we can record the edges as we traverse and then the last node is the end.

        # Actually, the above while loop is not correctly recording the trail. We are appending an edge for every time we pop, but the last node is not connected by an edge.

        # We need to record the trail as a list of nodes, then convert to edges.

        # Alternatively, we can use a different approach:

        # Let's do a DFS that collects the trail in reverse order (postorder). Then we reverse the entire trail.

        # But note: the problem requires the arrangement as a list of edges (pairs). The example output is a list of edges.

        # We can do:

        #   trail = []
        #   stack = [start]
        #   while stack:
        #       node = stack[-1]
        #       if graph[node]:
        #           next_node = graph[node].pop()
        #           stack.append(next_node)
        #       else:
        #           trail.append(stack.pop())
        
        #   Then, the trail is from end to start. Then we reverse the trail to get from start to end.

        # But note: the edges are not recorded. We need to record the edges.

        # We can record the edges by keeping track of the previous node.

        # Let me try a different method:

        # We'll use a stack to simulate the DFS and record the path (nodes) in reverse order.

        # Steps for Hierholzer (standard):

        #   Let's maintain a list `path` to record the trail (nodes) in the order visited.
        #   We start at `start` and then for each node, we choose an outgoing edge (remove it) and go to the neighbor.
        #   When we get stuck, we record the node and backtrack.

        #   Then, we reverse the path to get the trail from start to end.

        # However, the problem requires the output as a list of edges (pairs). So we can do:

        #   trail_nodes = []
        #   stack = [start]
        #   while stack:
        #       node = stack[-1]
        #       if graph[node]:
        #           next_node = graph[node].pop()
        #           stack.append(next_node)
        #       else:
        #           trail_nodes.append(stack.pop