class Solution:
    def isSubPath(self, head: Optional[ListNode], root: Optional[TreeNode]) -> bool:

        if head is None:
            return True

        if root is None:
            return False

        if head.val == root.val:
            if self.isSame(head, root):
                return True
            
        return self.isSubPath(head, root.left) or self.isSubPath(head, root.right)

    
    def isSame(self, head, root):

        if head is None:
            return True
        
        if root is None:
            return False

        if head.val == root.val: 
            return self.isSame(head.next, root.left) or self.isSame(head.next, root.right)
        
        return False