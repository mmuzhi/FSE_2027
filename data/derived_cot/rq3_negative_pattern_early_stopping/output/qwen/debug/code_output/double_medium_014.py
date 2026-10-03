class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]]) -> bool:
        # Build the graph: for each course, list of prerequisites (what this course depends on)
        graph = {i: [] for i in range(numCourses)}
        for a, b in prerequisites:
            # b depends on a, so add a to the list of b's prerequisites
            graph[b].append(a)
        
        # We'll use two sets: one for the recursion stack (currently visiting), and one for visited nodes (fully processed)
        # Alternatively, we can use a set for recursion stack and mark nodes as visited when we leave them.
        # But we'll use a set for recursion stack and a set for visited nodes.
        visited = set()
        rec_stack = set()
        
        def dfs(course):
            visited.add(course)
            rec_stack.add(course)
            for p in graph[course]:
                if p not in visited:
                    if not dfs(p):
                        return False
                elif p in rec_stack:
                    # Cycle detected
                    return False
            rec_stack.remove(course)
            return True
        
        for i in range(numCourses):
            if i not in visited:
                if not dfs(i):
                    return False
        return True