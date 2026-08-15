from typing import List
from collections import defaultdict

class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        pre = defaultdict(list)
        for course, p in prerequisites:
            pre[course].append(p)

        taken = set()
        done = set()

        def dfs(course):
            if course in done:
                return True
            if course in taken:
                return False
            if not pre[course]:
                done.add(course)
                return True

            taken.add(course)
            for p in pre[course]:
                if not dfs(p):
                    return False
            taken.remove(course)
            done.add(course)
            return True

        for course in range(numCourses):
            if not dfs(course):
                return False
        return True