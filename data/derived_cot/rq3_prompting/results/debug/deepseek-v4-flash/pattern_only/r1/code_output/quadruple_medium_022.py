class Solution:
    def smallestString(self, s: str) -> str:
        ct1 = 0
        for ch in s:
            if ch == 'a':
                ct1 += 1
            else:
                break

        ans = 'a' * ct1
        s = s[ct1:]
        change = False
        ct2 = 0

        for ch in s:
            ct2 += 1
            if ch != 'a':
                ans += chr(ord(ch) - 1)
                change = True
                continue
            else:
                ans += ch
                if change:
                    break

        if change:
            return ans + s[ct2:]
        return ans[:-1] + 'z'