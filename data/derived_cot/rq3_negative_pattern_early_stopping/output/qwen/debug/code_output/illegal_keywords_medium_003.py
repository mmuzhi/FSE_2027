import collections

class Solution:
    def closestMeetingNode(self, edges: List[int], node1: int, node2: int) -> int:
        n = len(edges)
        INF = float('inf')
        d1 = [INF] * n
        d2 = [INF] * n
        
        # BFS for node1
        q = collections.deque()
        d1[node1] = 0
        q.append(node1)
        while q:
            cur = q.popleft()
            nxt = edges[cur]
            if nxt != -1 and d1[nxt] == INF:
                d1[nxt] = d1[cur] + 1
                q.append(nxt)
                
        # BFS for node2
        q = collections.deque()
        d2[node2] = 0
        q.append(node2)
        while q:
            cur = q.popleft()
            nxt = edges[cur]
            if nxt != -1 and d2[nxt] == INF:
                d2[nxt] = d2[cur] + 1
                q.append(nxt)
                
        ans = -1
        min_max = INF
        for i in range(n):
            if d1[i] == INF or d2[i] == INF:
                continue
            candidate = max(d1[i], d2[i])
            if candidate < min_max:
                min_max = candidate
                ans = i
            elif candidate == min_max and i < ans:
                ans = i
                
        return ans