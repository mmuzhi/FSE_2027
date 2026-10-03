import sys
sys.setrecursionlimit(1 << 25)

MOD = 998244353

class Fenw:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n+1)

    def update(self, index, delta):
        # index is 1-indexed in Fenw tree? Actually, we'll use 1-indexed for the Fenw tree for numbers 1..n.
        i = index
        while i <= self.n:
            self.tree[i] = (self.tree[i] + delta) % MOD
            i += i & -i

    def query(self, index):
        # prefix sum from 1 to index
        s = 0
        i = index
        while i:
            s = (s + self.tree[i]) % MOD
            i -= i & -i
        return s

    def range_query(self, l, r):
        if l > r:
            return 0
        res = self.query(r) - self.query(l-1)
        return res % MOD

class SegmentTree:
    def __init__(self, n):
        self.n = n
        self.size = 1
        while self.size < n:
            self.size *= 2
        self.data = [10**9] * (2 * self.size)  # 10**9 is INF

    def build(self, arr):
        # not used in this solution, but we can build from an array if needed
        pass

    def update(self, index, value):
        # index is 0-indexed in the original array
        pos = index + self.size
        self.data[pos] = value
        while pos > 1:
            pos //= 2
            self.data[pos] = min(self.data[2*pos], self.data[2*pos+1])

    def query(self, l, r):
        # [l, r] inclusive, 0-indexed
        if l > r:
            return 10**9
        l += self.size
        r += self.size
        res = 10**9
        while l <= r:
            if l % 2 == 1:
                res = min(res, self.data[l])
                l += 1
            if r % 2 == 0:
                res = min(res, self.data[r])
                r -= 1
            l //= 2
            r //= 2
        return res

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    A = list(map(int, data[1:1+n]))
    
    # We'll use 0-indexed for the permutation indices and the array A.
    # We need to assign numbers from 1 to n to the indices 0 to n-1.
    
    # Initialize:
    assigned = [0] * n   # the permutation value at index i
    seg_tree = SegmentTree(n)   # for the minimum value in the segment of indices (0-indexed indices)
    fenw = Fenw(n)   # Fenw tree for available numbers (1-indexed numbers from 1 to n)
    
    # Initially, all numbers 1..n are available. We'll set the Fenw tree to have 1 for each number.
    # But note: our Fenw tree is for numbers 1..n, and we update by subtracting one when we use a number.
    # We'll initialize the Fenw tree with zeros and then add 1 for each number from 1 to n.
    # But we can also update the Fenw tree by adding 1 for each number from 1 to n.
    for i in range(1, n+1):
        fenw.update(i, 1)
    
    # We'll also maintain a list for the available numbers? Actually, the Fenw tree is enough for counting.
    
    # We'll process each index i from 0 to n-1.
    ans = 1
    for i in range(n):
        # Condition 1: segment [A[i], i-1] (if any)
        L = A[i]
        R = i-1
        if L <= R:
            M1 = seg_tree.query(L, R)
        else:
            M1 = 10**9   # INF
        
        # Condition 2: if A[i] > 0, then we require assigned[A[i]-1] < x
        if A[i] > 0:
            M2 = assigned[A[i]-1]
        else:
            M2 = -10**9   # -INF
        
        # The available numbers must be in (M2, M1) (if