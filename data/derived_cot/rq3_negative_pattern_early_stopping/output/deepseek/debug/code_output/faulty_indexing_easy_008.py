class Node:
    def __init__(self, val=None, children=None):
        self.val = val
        self.children = children

class Solution:
    def maxDepth(self, root: 'Node') -> int:
        if root is None:
            return 0
        depth = 0
        nodes_queue = [root]
        next_nodes_queue = []
        while nodes_queue:
            node_out = nodes_queue.pop(0)
            if node_out.children:
                for child in node_out.children:
                    next_nodes_queue.append(child)
            if not nodes_queue:
                nodes_queue, next_nodes_queue = next_nodes_queue, nodes_queue
                depth += 1
        return depth