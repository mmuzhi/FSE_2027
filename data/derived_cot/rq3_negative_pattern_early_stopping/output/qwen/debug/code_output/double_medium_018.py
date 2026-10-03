from collections import defaultdict

class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        pre = defaultdict(list)
        for a, b in prerequisites:
            pre[a].append(b)
        
        visited = set()
        stack = set()
        
        def dfs(course):
            visited.add(course)
            stack.add(course)
            for p in pre[course]:
                if p not in visited:
                    if not dfs(p):
                        return False
                elif p in stack:
                    return False
            stack.remove(course)
            return True
        
        for course in range(numCourses):
            if course not in visited:
                if not dfs(course):
                    return False
        return True