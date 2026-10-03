class Solution:
    def findKthBit(self, N, K, R = True):
        if K == 1: 
            return '0' if R else '1'
        mid = (1 << (N-2))
        if K <= mid:
            return self.findKthBit(N - 1, K, R)
        else:
            return self.findKthBit(N - 1, 2 * mid - K, not R)
