import heapq
import sys

def main():
    data = sys.stdin.read().split()
    it = iter(data)
    n = int(next(it)); m = int(next(it)); X = int(next(it))
    graph = [[] for _ in range(n+1)]
    for _ in range(m):
        u = int(next(it)); v = int(next(it))
        graph[u].append(v)
    
    # Build the reversed graph (transpose) for state1
    rev_graph = [[] for _ in range(n+1)]
    for u in range(1, n+1):
        for v in graph[u]:
            rev_graph[v].append(u)
    
    # We'll use Dijkstra on a graph with 2*n nodes: node i in state0 and node i in state1.
    # We'll represent state0 as node i, and state1 as node i + n.
    # But note: we have two graphs: original and reversed. We need to consider both.
    # We'll set up a 2D array for distances: dist[i][0] for state0, dist[i][1] for state1.
    INF = 10**18
    dist = [[INF] * 2 for _ in range(n+1)]
    dist[1][0] = 0
    
    # Priority queue: (cost, node, state)
    heap = []
    heapq.heappush(heap, (0, 1, 0))
    
    while heap:
        cost, node, state = heapq.heappop(heap)
        if cost != dist[node][state]:
            continue
        # If we are at node N, we can break early? But we need to consider both states.
        if node == n:
            # But we might have a lower cost in the other state? So we don't break.
            continue
        
        # Two operations: move or reverse.
        # Operation 1: move (if state0, then use original graph; if state1, then use reversed graph)
        if state == 0:
            # In state0, we can move to any neighbor in the original graph (node, state0) with cost+1.
            for neighbor in graph[node]:
                new_cost = cost + 1
                if new_cost < dist[neighbor][0]:
                    dist[neighbor][0] = new_cost
                    heapq.heappush(heap, (new_cost, neighbor, 0))
        else:
            # In state1, we can move to any neighbor in the reversed graph (node, state1) with cost+1.
            for neighbor in rev_graph[node]:
                new_cost = cost + 1
                if new_cost < dist[neighbor][1]:
                    dist[neighbor][1] = new_cost
                    heapq.heappush(heap, (new_cost, neighbor, 1))
        
        # Operation 2: reverse (cost X) to switch state (same node)
        new_state = 1 - state
        new_cost = cost + X
        if new_cost < dist[node][new_state]:
            dist[node][new_state] = new_cost
            heapq.heappush(heap, (new_cost, node, new_state))
    
    # The answer is the minimum of dist[n][0] and dist[n][1]
    print(min(dist[n][0], dist[n][1]))

if __name__ == "__main__":
    main()