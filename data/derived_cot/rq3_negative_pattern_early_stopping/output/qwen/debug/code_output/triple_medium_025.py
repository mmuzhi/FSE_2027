from collections import deque

class Solution:
    def closestMeetingNode(self, edges: List[int], node1: int, node2: int) -> int:
        INF = float('inf')
        n = len(edges)
        dist1 = [INF] * n
        dist2 = [INF] * n
        
        # BFS for node1
        q = deque()
        q.append(node1)
        dist1[node1] = 0
        while q:
            cur = q.popleft()
            nxt = edges[cur]
            if nxt == -1:
                continue
            if dist1[nxt] == INF:
                dist1[nxt] = dist1[cur] + 1
                q.append(nxt)
        
        # BFS for node2
        q = deque()
        q.append(node2)
        dist2[node2] = 0
        while q:
            cur = q.popleft()
            nxt = edges[cur]
            if nxt == -1:
                continue
            if dist2[nxt] == INF:
                dist2[nxt] = dist2[cur] + 1
                q.append(nxt)
        
        ans = -1
        min_max = INF
        for i in range(n):
            if dist1[i] != INF and dist2[i] != INF:
                m = max(dist1[i], dist2[i])
                if m < min_max:
                    min_max = m
                    ans = i
                elif m == min_max:
                    if i < ans:
                        ans = i
        
        return ans