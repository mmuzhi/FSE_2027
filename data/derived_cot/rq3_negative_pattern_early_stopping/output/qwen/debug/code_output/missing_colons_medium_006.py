class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        # Build the graph with all courses from 0 to numCourses-1
        pre = {i: [] for i in range(numCourses)}
        for a, b in prerequisites:
            pre[b].append(a)  # b requires a

        taken = set()

        def dfs(course):
            if course in taken:
                return False
            if not pre[course]:
                taken.add(course)
                return True

            taken.add(course)
            for p in pre[course]:
                if not dfs(p):
                    return False
            taken.add(course)  # This line is redundant because we already added course above, but we are adding again. We can remove this.
            return True

        for course in range(numCourses):
            if not dfs(course):
                return False
        return True