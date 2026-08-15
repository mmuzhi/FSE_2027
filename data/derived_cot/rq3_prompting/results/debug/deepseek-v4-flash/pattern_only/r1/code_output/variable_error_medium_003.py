from typing import List

class Solution:
    def getFolderNames(self, names: List[str]) -> List[str]:
        ans = []
        seen = {}

        for name in names:
            if name not in seen:
                ans.append(name)
                seen[name] = 1
            else:
                k = seen[name]
                while name + "(" + str(k) + ")" in seen:
                    k += 1
                seen[name] = k + 1
                new_name = name + "(" + str(k) + ")"
                ans.append(new_name)
                seen[new_name] = 1

        return ans