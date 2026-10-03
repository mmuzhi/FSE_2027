class Line:
    __slots__ = ('a', 'b')
    def __init__(self, a, b):
        self.a = a
        self.b = b
    def eval(self, x):
        return self.a * x + self.b

class LiChaoTree:
    def __init__(self, low, high):
        self.low = low
        self.high = high
        self.line = None
        self.left = None
        self.right = None

    def insert(self, line):
        if self.line is None:
            self.line = line
            return
        mid = (self.low + self.high) // 2
        if line.eval(mid) > self.line.eval(mid):
            self.line, line = line, self.line
        if self.low == self.high:
            return
        if line.eval(self.low) > self.line.eval(self.low):
            if self.left is None:
                self.left = LiChaoTree(self.low, mid)
            self.left.insert(line)
        if line.eval(self.high) > self.line.eval(self.high):
            if self.right is None:
                self.right = LiChaoTree(mid+1, self.high)
            self.right.insert(line)

    def query(self, x):
        res = -10**18
        if self.line is not None:
            res = self.line.eval(x)
        if self.left and x <= (self.low + self.high) // 2:
            res = max(res, self.left.query(x))
        if self.right and x > (self.low + self.high) // 2:
            res = max(res, self.right.query(x))
        return res

class Solution:
    def findMaximumScore(self, nums: List[int]) -> int:
        n = len(nums)
        # If n is 1, then no jump is needed, score 0.
        if n == 1:
            return 0
        
        # Initialize the LiChao tree for the range [0, n] (x from 0 to n)
        tree = LiChaoTree(0, n)
        # dp[0] = 0, insert the line for index 0
        tree.insert(Line(nums[0], 0))
        
        # We'll compute dp[i] for i from 1 to n-1
        # But note: the dp[i] is computed from the tree query at i, and then we insert the line for i.
        # However, the recurrence is: dp[i] = max_{j < i} { dp[j] + (i - j)*nums[j] }
        # But we are storing the line for j as: f_j(x) = x * nums[j] + (dp[j] - j * nums[j])
        # Then, querying at x=i gives the maximum value.
        # But note: the dp[i] is the score to reach i, and then we use it to insert the line for i.
        # But the line for i is: f_i(x) = x * nums[i] + (dp[i] - i * nums[i])
        # We need to compute dp[i] for i from 1 to n-1.
        # However, the tree currently only has lines for j=0. Then for i=1, we query and get dp[1], then insert line for i=1.
        # But then for i=2, we query and get dp[2] from all j<2 (j=0 and j=1).
        # But note: the dp[0] is 0, and the line for 0 is already inserted.
        # We need to compute dp[i] for i from 1 to n-1.
        # But the above insertion for j=0 is done. Then for i=1, we query and get dp[1], then insert the line for i=1.
        # But the dp[i] is the score to reach i, and then we use it to insert the line for i.
        # But the recurrence is correct.

        # However, we need to compute dp[i] for i from 1 to n-1. But the above tree only has the line for j=0 inserted initially.
        # Then for i=1, we query and get dp[1] = max_{j<1} { dp[j] + (1-j)*nums[j] } = dp[0] + (1-0)*nums[0] = 0 + 1*nums[0] = nums[0].
        # Then, we insert the line for i=1: slope = nums[1], intercept = dp[1] - 1 * nums[1] = nums[0] - nums[1].
        # Then for i=2, we query and get dp[2] = max( dp[0] + (2-0