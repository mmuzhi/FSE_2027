from collections import defaultdict
from typing import List

class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        pre = defaultdict(list)
        for course, p in prerequisites:
            pre[course].append(p)
        
        taken = set()
        visited = set()  # to memoize fully processed nodes

        def dfs(course):
            if course in visited:
                return True
            if not pre[course]:
                visited.add(course)
                return True       
            if course in taken:
                return False       
            taken.add(course)
            for p in pre[course]:
                if not dfs(p): 
                    return False        
            taken.remove(course)
            visited.add(course)
            return True
        
        for course in range(numCourses):
            if not dfs(course):
                return False
        return True