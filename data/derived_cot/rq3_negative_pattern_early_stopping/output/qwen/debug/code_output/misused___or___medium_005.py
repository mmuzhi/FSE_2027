# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def isSubPath(self, head: Optional[ListNode], root: Optional[TreeNode]) -> bool:

        if head is None:
            return True

        if root is None:
            return False

        if head.val == root.val:
            if self.checkPath(head.next, root.left) or self.checkPath(head.next, root.right):
                return True

        return self.isSubPath(head, root.left) or self.isSubPath(head, root.right)
    
    def checkPath(self, head, root):
        if head is None:
            return True
        if root is None:
            return False
        if head.val != root.val:
            return False
        # We have matched the current node, now check the rest of the linked list in the left or right subtree.
        return self.checkPath(head.next, root.left) or self.checkPath(head.next, root.right)