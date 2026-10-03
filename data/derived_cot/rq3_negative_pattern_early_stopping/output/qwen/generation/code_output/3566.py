class Solution:
    def stringSequence(self, target: str) -> List[str]:
        s = ""
        res = [s]
        for char in target:
            # If the current string is empty, we must press key1 to add 'a'
            if not s:
                s = 'a'
                res.append(s)