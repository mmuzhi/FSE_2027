from typing import List
from collections import defaultdict

class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        pre = defaultdict(list)
        for course, p in prerequisites:
            pre[course].append(p)

        visited = [0] * numCourses  # 0 = unvisited, 1 = visiting, 2 = visited

        def dfs(course: int) -> bool:
            if visited[course] == 1:
                return False
            if visited[course] == 2:
                return True

            visited[course] = 1
            for p in pre[course]:
                if not dfs(p):
                    return False
            visited[course] = 2
            return True

        for course in range(numCourses):
            if not dfs(course):
                return False
        return True