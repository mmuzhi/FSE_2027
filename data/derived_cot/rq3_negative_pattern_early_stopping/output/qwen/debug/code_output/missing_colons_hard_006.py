import collections

class Solution:
    def kSimilarity(self, s1: str, s2: str) -> int:
        if s1 == s2:
            return 0
        
        deque = collections.deque()
        deque.append(s1)
        seen = set()
        seen.add(s1)
        answ = 0
        
        while deque:
            size = len(deque)
            for _ in range(size):
                string = deque.popleft()
                if string == s2:
                    return answ
                
                i = 0
                while i < len(string) and string[i] == s2[i]:
                    i += 1
                
                for j in range(i+1, len(string)):
                    if string[i] == s2[j] and string[j] == s2[i]:
                        new_string = string[:i] + string[j] + string[i+1:j] + string[i] + string[j+1:]
                        if new_string not in seen:
                            seen.add(new_string)
                            deque.append(new_string)
            answ += 1
        
        return answ