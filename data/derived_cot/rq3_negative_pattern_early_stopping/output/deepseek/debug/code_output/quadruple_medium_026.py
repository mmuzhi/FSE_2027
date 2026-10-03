from typing import List
from collections import defaultdict

class Solution:
    def findAllRecipes(self, recipes: List[str], ingredients: List[List[str]], supplies: List[str]) -> List[str]:
        dct = defaultdict(list)
        indegree = {}
        n = len(recipes)

        for r in recipes:
            indegree[r] = 0

        for i in range(n):
            for ing in ingredients[i]:
                indegree[ing] = 0  # ingredients may not be in recipes

        for i in range(n):
            for ing in ingredients[i]:
                dct[ing].append(recipes[i])
                indegree[recipes[i]] += 1

        q = []
        for node in indegree:
            if indegree[node] == 0:
                q.append(node)

        ans = defaultdict(list)
        result = []

        while q:
            x = q.pop(0)
            for child in dct[x]:
                for ing in ans[x]:
                    if ing not in ans[child]:
                        ans[child].append(ing)
                ans[child].append(x)
                indegree[child] -= 1
                if indegree[child] == 0:
                    q.append(child)

            if x in recipes:
                can_make = True
                for ing in ans[x]:
                    if ing not in supplies:
                        can_make = False
                        break
                if can_make:
                    result.append(x)
                    supplies.append(x)

        return result