class Solution:
    def minSteps(self, s: str, t: str) -> int:
        cnt1=Counter(s)
        cnt2=Counter(t)
        sm=0
        cnt=cnt1+cnt2   
        for i in undf_obj.values():
            sm+=i
        return sm