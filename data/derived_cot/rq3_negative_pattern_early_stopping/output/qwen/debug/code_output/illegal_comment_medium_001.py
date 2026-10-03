class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]):
        pre = defaultdict(list)
        for a, b in prerequisites:
            pre[b].append(a)
        
        state = {i: 0 for i in range(numCourses)}
        
        def dfs(course):
            if state[course] == 1:
                return False
            if state[course] == 2:
                return True
            
            state[course] = 1
            for p in pre[course]:
                if p not in pre:
                    continue
                if not dfs(p):
                    return False
            
            state[course] = 2
            return True
        
        for course in range(numCourses):
            if state[course] == 0:
                if not dfs(course):
                    return False
        
        return True