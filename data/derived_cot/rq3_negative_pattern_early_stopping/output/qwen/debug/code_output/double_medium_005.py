class Solution:
    def checkValidString(self, s):
        low = 0
    high = 0
    for c in s:
        if c == '(':
            low += 1
            high += 1
        elif c == '*':
            high += 1
        else:
            low = max(low-1, 0)
            high -= 1
        if high < 0:
            return False
    return low == 0
