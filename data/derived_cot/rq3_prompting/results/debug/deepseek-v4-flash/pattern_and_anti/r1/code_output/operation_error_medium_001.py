from typing import List
from collections import defaultdict, deque

class Solution:
    def findAllRecipes(self, recipes: List[str], ingredients: List[List[str]], supplies: List[str]) -> List[str]:
        graph = defaultdict(list)
        indegree = {}

        for recipe, ing_list in zip(recipes, ingredients):
            indegree[recipe] = len(ing_list)
            for ing in ing_list:
                graph[ing].append(recipe)

        ans = []
        q = deque()
        seen = set()

        for s in supplies:
            q.append(s)
            seen.add(s)

        for r in recipes:
            if indegree[r] == 0:
                ans.append(r)
                if r not in seen:
                    q.append(r)
                    seen.add(r)

        while q:
            item = q.popleft()
            for r in graph[item]:
                indegree[r] -= 1
                if indegree[r] == 0:
                    ans.append(r)
                    if r not in seen:
                        q.append(r)
                        seen.add(r)

        return ans