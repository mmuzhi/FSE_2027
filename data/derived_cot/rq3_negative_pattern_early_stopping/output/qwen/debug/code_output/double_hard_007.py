class Solution:
    def validArrangement(self, pairs: List[List[int]]) -> List[List[int]]:
        graph = defaultdict(list)
        degree = defaultdict(int) # net out-degree: out-degree - in-degree
        for x, y in pairs:
            graph[x].append(y)
            degree[x] += 1
            degree[y] -= 1
        
        # Find the start node: the node with net out-degree 1 (if exists) or if not, then any node with non-zero degree?
        # But note: the Eulerian trail condition: exactly one node with net out-degree 1, one with net out-degree -1, and others 0.
        # However, the code breaks at the first node that is not 1. But what if there are multiple nodes with non-zero degree?
        # We should check that there is exactly one node with net out-degree 1 and one with -1, and the rest 0.
        # But the problem says "validArrangement", so we assume the input is such that an Eulerian trail exists.

        # Let's find the start node: the node with net out-degree 1. If none, then we can start from any node (if Eulerian circuit) but then we need to check for balanced graph.
        start = None
        for node, d in degree.items():
            if d == 1:
                start = node
                break
        else:
            # If no node with net out-degree 1, then we try to find a node with non-zero degree (if any) for Eulerian circuit?
            # But note: in Eulerian circuit, all nodes have net out-degree 0. So if we don't find a node with 1, then we must have all zeros.
            # However, the code above breaks at the first node that is not 1. But if all are 1? Then we break at the first node and use that as start.
            # Actually, the condition for Eulerian trail is that there is exactly one node with net out-degree 1 and one with -1. 
            # So if we don't find a node with 1, then we might have an Eulerian circuit? But then we can start from any node.
            # However, the code above breaks at the first node that is not 1. In Eulerian circuit, all nodes have 0, so we break at the first node and use that as start? 
            # But then we are not guaranteed to have an Eulerian trail. We must check the condition.

            # Actually, the problem does not specify that the graph is connected. But we assume the graph is connected for Eulerian trail.

            # Let's change the approach: we must have exactly one node with net out-degree 1 and one with -1, or all zeros (Eulerian circuit).

            # We'll find the start node by checking the condition.

            # If we didn't find a node with 1, then we look for a node with non-zero degree (if any) and use that as start? But that might not be correct.

            # Actually, the code above is flawed. We should first check the condition of the graph.

            # Since the problem says "validArrangement", we assume the graph has an Eulerian trail. So we must have exactly two nodes with non-zero net out-degree: one 1 and one -1, or all zeros.

            # Let's count the net out-degrees:
            non_zero = [d for d in degree.values() if d != 0]
            if len(non_zero) == 0:
                # Eulerian circuit: all nodes have net out-degree 0. We can start from any node, say the first node in the graph.
                start = next(iter(degree.keys()))
            elif len(non_zero) == 2 and all(d in (1, -1) for d in non_zero):
                # Then we have one node with 1 and one with -1.
                # But note: the code above breaks at the first node that is not 1. So if we have a node with -1, then we break at the first node (which might be the one with 1) and then use that as start? 
                # Actually, the code above breaks at the first node that is not 1. So if we have a node with 1 and a node with -1, then the node with 1 is found first and used as start.
                # But what if the node with 1 is not the first in the iteration? Then we break at the node with -1 (which is not 1) and use that as start? That would be wrong.

                # We need to find the node with net out-degree 1. If we don't find one, then we look for the node with net out-degree -1? But the condition requires one node with