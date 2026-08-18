class Solution:
    def checkValidString(self, s):
        st = []
        sr = []
        for i in range(len(s)):
            if s[i] == '(':
                st.append(i)
            elif s[i] == '*':
                sr.append(i)
            else:
                if st:
                    st.pop()
                elif sr:
                    sr.pop()
                else:
                    return False
        while st:
            if len(sr) == 0:
                return False
            elif sr[-1] > st[-1]:
                st.pop()
                sr.pop()
            else:
                return False
        return True