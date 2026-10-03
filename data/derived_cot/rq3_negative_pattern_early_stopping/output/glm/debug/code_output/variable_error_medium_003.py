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
                while True:
                    new_name = name + '(' + str(k) + ')'
                    if new_name not in seen:
                        ans.append(new_name)
                        seen[new_name] = 1
                        break
                    else:
                        k += 1
                seen[name] = k + 1
        return ans