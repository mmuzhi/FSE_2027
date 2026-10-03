import collections

class Solution:
    def closestMeetingNode(self, edges: List[int], node1: int, node2: int) -> int:
        n = len(edges)
        INF = float('inf')
        dist1 = [INF] * n
        dist2 = [INF] * n

        # BFS for node1
        q = collections.deque()
        dist1[node1] = 0
        q.append(node1)
        while q:
            cur = q.popleft()
            nxt = edges[cur]
            if nxt != -1 and dist1[nxt] == INF:
                dist1[nxt] = dist1[cur] + 1
                q.append(nxt)

        # BFS for node2
        q = collections.deque()
        dist2[node2] = 0
        q.append(node2)
        while q:
            cur = q.popleft()
            nxt = edges[cur]
            if nxt != -1 and dist2[nxt] == INF:
                dist2[nxt] = dist2[cur] + 1
                q.append(nxt)

        ans = -1
        min_d = INF
        for i in range(n):
            if dist1[i] != INF and dist2[i] != INF:
                d = max(dist1[i], dist2[i])
                if d < min_d:
                    min_d = d
                    ans = i
                elif d == min_d and i < ans:
                    ans = i

        return ans