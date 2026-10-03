from typing import List

class Solution:
    def getFolderNames(self, names: List[str]) -> List[str]:
        ans = []  
        seen = {}

        for name in names:
            if name not in seen:
                ans.append(name)
                seen[name] = 0
            else:
                k = seen[name]
                while True:
                    new_name = name + '(' + str(k) + ')'
                    if new_name not in seen:
                        ans.append(new_name)
                        seen[new_name] = 0  # We don't need to track the count for the new_name? Actually, we don't need to, but we need to mark it as used.
                        # But note: we are not updating the base name's count. We are only using the base name's count to form the new_name.
                        # After forming the new_name, we should update the base name's count to k+1 so that next time we start from k+1.
                        seen[name] = k + 1
                        break
                    else:
                        k += 1
        return ans