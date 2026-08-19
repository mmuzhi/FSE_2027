class Solution:
    def f(self,n,r,count):
        if count==32:return r
        return self.f(n<<1,(r<<1)|(n&1),count+1)
    def reverseBits(self, n: int) -> int:return self.f(n,0,0)