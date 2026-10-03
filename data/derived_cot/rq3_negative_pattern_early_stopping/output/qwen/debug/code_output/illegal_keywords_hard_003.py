from queue import Queue

class Solution:
    def frogPosition(self, n: int, edges: List[List[int]], t: int, target: int) -> float:
        if n == 0:
            return 0.0
        
        graph = [[] for _ in range(n+1)]
        for edge in edges:
            u, v = edge
            graph[u].append(v)
            graph[v].append(u)
        
        if target == 1:
            # If target is 1, then we are at the start. But we must make t jumps.
            # However, if t==0, then we are at 1. But if t>=1, we leave 1 and then cannot come back? 
            # But the problem says the frog makes t jumps. So if t==0, then we are at 1. Otherwise, we leave.
            # But note: the problem doesn't specify t==0. Let's assume t>=0.
            # However, the code below uses BFS for t steps. We'll handle it in BFS.
            pass
        
        # We'll use BFS for t steps.
        # We need to consider that the frog starts at node 1 at time 0.
        # We are to compute the probability that after t jumps, the frog is at the target.
        # We'll do BFS for t steps, and at each node, we record the probability and the time.
        # But note: the frog must make exactly t jumps. So we are interested in the state at time t.

        # We'll use a queue that stores (node, time, probability)
        # But note: the frog can only jump to unvisited nodes? The problem doesn't say, but the code uses a visited array.
        # However, the problem statement is not provided. We'll assume that the frog cannot revisit nodes.

        # We'll use a visited array to mark nodes that have been visited (at any time). But note: if we visit a node at time k, then we cannot visit it again at a later time.

        # But wait: the frog must make t jumps. So if we are at a node at time k, then we can only jump to unvisited nodes at time k+1.

        # We'll do BFS for t steps.

        # However, note: the frog starts at node 1 at time 0. Then at time 1, it jumps to a neighbor, etc.

        # We'll use a queue and a visited array (or set) to mark nodes that have been visited (so we don't revisit).

        # But note: the problem says the frog makes t jumps. So we are only interested in the state at time t.

        # We'll do BFS for t steps, and at each step, we mark the node as visited and then we don't allow going back.

        # However, the code provided does not use a visited set for the entire BFS, but marks nodes as visited and then doesn't allow visiting again.

        # Let's fix the code:

        # We'll use a visited array (list of booleans) of size n+1.
        visited = [False] * (n+1)
        # We'll use a queue that stores (node, time, probability)
        q = Queue()
        q.put((1, 0, 1.0))
        visited[1] = True

        # We'll do BFS for t steps (from time 0 to time t)
        # But note: at time 0, we are at node 1. Then we do t jumps, so we are at time t.

        # However, the code provided uses a different approach: it does t iterations, each iteration being a jump.

        # Let's restructure:

        # We'll do t steps (each step is a jump). At each step, we process all nodes at the current time (which is the step number).

        # But note: the frog starts at time 0, so after t jumps, the time is t.

        # We'll do:

        #   for time_step in range(1, t+1):
        #       process all nodes at time_step-1 to get nodes at time_step.

        # However, the provided code uses a loop for dur in range(t) and then processes the queue (which initially has the start node).

        # But the provided code has a bug: it marks the node as visited when we first encounter it, and then we don't allow going back.

        # We'll fix the code by:

        #   Using a visited array to mark nodes that have been visited (so we don't revisit).
        #   We do BFS for t steps.

        # However, note: the frog must make exactly t jumps. So we are only interested in the state at time t.

        # We'll change the code to use a visited array and BFS for t