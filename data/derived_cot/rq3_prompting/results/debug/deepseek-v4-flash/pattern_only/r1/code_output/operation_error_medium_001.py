from typing import List
from collections import defaultdict, deque

class Solution:
    def findAllRecipes(self, recipes: List[str], ingredients: List[List[str]], supplies: List[str]) -> List[str]:
        recipe_set = set(recipes)
        indegree = {recipe: len(ingredients[i]) for i, recipe in enumerate(recipes)}
        graph = defaultdict(list)

        for recipe, ing_list in zip(recipes, ingredients):
            for ing in ing_list:
                graph[ing].append(recipe)

        available = set()
        q = deque()

        for s in supplies:
            if s not in available:
                available.add(s)
                q.append(s)

        for recipe in recipes:
            if indegree[recipe] == 0 and recipe not in available:
                q.append(recipe)
                available.add(recipe)

        ans = []
        while q:
            item = q.popleft()

            if item in recipe_set:
                ans.append(item)

            for recipe in graph[item]:
                indegree[recipe] -= 1
                if indegree[recipe] == 0 and recipe not in available:
                    q.append(recipe)
                    available.add(recipe)

        return ans