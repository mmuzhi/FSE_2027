class Solution():
    def restoreIpAddresses(self, s: str) -> List[str]:
        res = []
        cur = []
        n = len(s)
        
        def backtrack(i):
            if i == n and len(cur) == 4:
                res.append(".".join(cur))
                return
            if len(cur) > 4 or i >= n:
                return
            if s[i] == '0':
                cur.append('0')
                backtrack(i + 1)
                cur.pop()
                return
            j = 0
            while j < 3 and i + j < n:
                num = s[i:i+j+1]
                if int(num) < 256:
                    cur.append(num)
                    backtrack(i + j + 1)
                    cur.pop()
                j += 1
        
        backtrack(0)
        return res