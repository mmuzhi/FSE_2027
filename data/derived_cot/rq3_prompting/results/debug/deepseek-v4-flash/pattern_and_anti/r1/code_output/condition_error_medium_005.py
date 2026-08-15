from typing import List, Optional

class Solution:
    def buildTree(self, inorder: List[int], postorder: List[int]) -> Optional[TreeNode]:
        inorder_map = {val: idx for idx, val in enumerate(inorder)}
        postorder_idx = len(postorder) - 1

        def treeHelper(left: int, right: int) -> Optional[TreeNode]:
            nonlocal postorder_idx
            if left > right:
                return None

            node_val = postorder[postorder_idx]
            root = TreeNode(node_val)
            postorder_idx -= 1

            inorder_index = inorder_map[node_val]

            root.right = treeHelper(inorder_index + 1, right)
            root.left = treeHelper(left, inorder_index - 1)

            return root

        return treeHelper(0, len(inorder) - 1)