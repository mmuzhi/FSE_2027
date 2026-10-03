from typing import List
from collections import defaultdict

class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        pre = defaultdict(list)
        for course, p in prerequisites:
            pre[course].append(p)
        
        taken = set()  # nodes currently on recursion stack
        
        def dfs(course):
            if not pre[course]:  # no prerequisites
                return True
            if course in taken:
                return False
            taken.add(course)
            for p in pre[course]:
                if not dfs(p):
                    return False
            taken.remove(course)
            pre[course] = []  # mark as processed
            return True
        
        for course in range(numCourses):
            if not dfs(course):
                return False
        return True