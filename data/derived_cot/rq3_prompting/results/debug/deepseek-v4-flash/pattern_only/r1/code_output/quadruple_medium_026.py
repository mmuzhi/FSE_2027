from typing import List
from collections import defaultdict, deque

class Solution:
    def findAllRecipes(self, recipes: List[str], ingredients: List[List[str]], supplies: List[str]) -> List[str]:
        graph = defaultdict(list)
        indegree = {}
        n = len(recipes)

        for r in recipes:
            indegree[r] = 0

        for ing_list in ingredients:
            for ing in ing_list:
                indegree.setdefault(ing, 0)

        for i in range(n):
            for ing in ingredients[i]:
                graph[ing].append(recipes[i])
                indegree[recipes[i]] += 1

        q = deque()
        for node in indegree:
            if indegree[node] == 0:
                q.append(node)

        ans = defaultdict(list)
        made = []
        available = set(supplies)
        recipe_set = set(recipes)

        while q:
            x = q.popleft()

            for recipe in graph[x]:
                ans[recipe].append(x)
                indegree[recipe] -= 1
                if indegree[recipe] == 0:
                    q.append(recipe)

            if x in recipe_set:
                for dep in ans[x]:
                    if dep not in available:
                        break
                else:
                    made.append(x)
                    available.add(x)

        return made