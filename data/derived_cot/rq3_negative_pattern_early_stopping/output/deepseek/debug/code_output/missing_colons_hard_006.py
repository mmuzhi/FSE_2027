import collections

class Solution:
    def kSimilarity(self, s1: str, s2: str) -> int:
        deque = collections.deque([s1])
        seen = {s1}
        ans = 0
        
        while deque:
            for _ in range(len(deque)):
                curr = deque.popleft()
                if curr == s2:
                    return ans
                
                i = 0
                while i < len(curr) and curr[i] == s2[i]:
                    i += 1
                
                for j in range(i + 1, len(curr)):
                    if curr[j] == s2[i] and curr[j] != s2[j]:
                        new = curr[:i] + curr[j] + curr[i+1:j] + curr[i] + curr[j+1:]
                        if new not in seen:
                            seen.add(new)
                            deque.append(new)
            ans += 1