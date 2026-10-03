def tsum(root):
    if(root==None):
        return 0
    x= root.val+tsum(root.left)+tsum(root.right)
    return x
def fun(root,sm,mx):
    if(root==None):
        return 0
    a=fun(root.left,sm,mx)
    b=fun(root.right,sm,mx)
    mx[0]=max(mx[0],a*(sm-a),b*(sm-b))
    return a+b+root.val
    
class Solution:
    def maxProduct(self, root: Optional[TreeNode]) -> int:
        mx=[0]
        sm=tsum(root)
        memo={}
        fun(root,sm,mx)
        return mx[0]%(10**9+7)