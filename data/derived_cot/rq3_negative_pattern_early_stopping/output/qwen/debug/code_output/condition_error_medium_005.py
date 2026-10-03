class Solution:
    def buildTree(self, inorder: List[int], postorder: List[int]) -> Optional[TreeNode]:
        if not inorder or not postorder:
            return None
        
        inorder_map = {val: idx for idx, val in enumerate(inorder)}
        
        def treeHelper(left, right, left_post, right_post):
            if left > right:
                return None
            
            node_val = postorder[right_post]
            root = TreeNode(node_val)
            inorder_index = inorder_map[node_val]
            
            left_post_segment_length = inorder_index - left
            right_post_segment_length = right - inorder_index
            
            root.left = treeHelper(left, inorder_index-1, left_post, left_post + left_post_segment_length - 1)
            root.right = treeHelper(inorder_index+1, right, left_post + left_post_segment_length, right_post-1)
            
            return root
        
        return treeHelper(0, len(inorder)-1, 0, len(postorder)-1)
