from typing import List
from collections import defaultdict

class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        pre = defaultdict(list)
        for course, p in prerequisites:
            pre[course].append(p)

        visited = set()      # courses fully processed (no cycle from them)
        in_stack = set()     # courses currently on recursion stack

        def dfs(course: int) -> bool:
            if course in in_stack:
                return False   # cycle detected
            if course in visited:
                return True    # already proved acyclic

            in_stack.add(course)
            for p in pre[course]:
                if not dfs(p):
                    return False
            in_stack.remove(course)

            visited.add(course)
            pre[course] = []
            return True

        for course in range(numCourses):
            if not dfs(course):
                return False
        return True