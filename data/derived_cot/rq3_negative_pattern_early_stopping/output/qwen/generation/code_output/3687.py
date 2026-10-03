class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        import collections
        n = len(nums)
        graph = [[] for _ in range(n)]
        for u, v, l in edges:
            graph[u].append((v, l))
            graph[v].append((u, l))
        
        parent = [-1] * n
        depth = [-1] * n
        depth[0] = 0
        stack = [0]
        while stack:
            node = stack.pop()
            for neighbor, l in graph[node]:
                if neighbor == parent[node]:
                    continue
                parent[neighbor] = node
                depth[neighbor] = depth[node] + 1
                stack.append(neighbor)
        
        children = [[] for _ in range(n)]
        for i in range(1, n):
            children[parent[i]].append(i)
        
        # Build a frequency dictionary for node values along a path, but we need to track uniqueness.
        # We'll do a DFS from the root and for each node, we can track the path from root to current node.
        # But n can be up to 50000, so we need an efficient way.
        # Instead, we can use a DFS that returns the maximum length and the minimum node count for the longest path from the root to the current node that satisfies the uniqueness condition.

        # However, note: the path must be downward and the uniqueness condition applies to all nodes in the path. But the path doesn't necessarily have to start at the root. It can start at any ancestor and go to a descendant. But note: the problem says "downward path from an ancestor node to a descendant node". So the path must be from an ancestor (which could be any node) to a descendant (so the entire path is from some node to a node in its subtree). But the uniqueness condition must hold for all nodes in the path.

        # But note: the path can start and end at the same node. So a single node is a valid path.

        # We need to consider all paths that are downward and have unique node values.

        # Approach:
        # 1. Root the tree at 0.
        # 2. We need to consider paths that start at any node and go downward (so from a node to one of its descendants). The condition is that all node values in the path are unique.

        # However, the problem asks for the longest path (by edge length) and then the minimum number of nodes in the paths of that maximum length.

        # We can think of it as: for each node, we want to know the longest path starting from that node (going downward) that has unique node values. But note: the path must be downward, so we can only go from a node to its children.

        # But the uniqueness condition: the entire path must have unique node values. So if we start at node u, then the path u -> v -> ... must have all distinct nums.

        # We can do a DFS from the root and for each node, we can track the frequency of node values in the path from the root to the current node. But then, when backtracking, we remove the current node's value. However, the path doesn't necessarily have to start at the root. It can start at any node. But note: the path is from an ancestor to a descendant. So the entire path is contained in the subtree of the starting node.

        # Actually, we can reframe: the path must be a contiguous downward path from some node to a descendant. The uniqueness condition must hold for the entire path.

        # We can do a DFS that for each node, we try to extend the path from its parent. But we need to know the uniqueness condition. We can maintain a frequency map for the path from the root to the current node, but then if we start the path at a node that is not the root, we cannot use the root's frequency map.

        # Alternatively, we can consider: for each node, we want to compute the longest path (in terms of edge length) that starts at that node and goes downward with unique node values. Then, the overall longest path is the maximum over all nodes of the path starting at that node.

        # But note: the path can start at any node, not necessarily the root. So we need to consider all nodes as potential starting points.

        # However, the tree is rooted at 0, and the path must be downward. So the starting node must be an ancestor of the ending node.

        # We can do a DFS from the root and for each node, we can compute the longest path that starts at that node and goes downward with unique node values. Then, we take the maximum edge length from all nodes.

        # But the uniqueness condition: the entire path must have unique node values.