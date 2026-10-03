"""
# Definition for a Node.
class Node:
    def __init__(self, val=None, children=None):
        self.val = val
        self.children = children

class Solution:
    def maxDepth(self, root: 'Node') -> int:
        if root == None:
            return 0
        depth = 0
        nodes_queue = [root]
        next_nodes_queue = []
        while nodes_queue:
            # Process the entire current level
            for node in nodes_queue:
                for child in node.children:
                    next_nodes_queue.append(child)
            # After processing the entire current level, switch to the next level
            nodes_queue, next_nodes_queue = next_nodes_queue, []
            depth += 1
        return depth
"""