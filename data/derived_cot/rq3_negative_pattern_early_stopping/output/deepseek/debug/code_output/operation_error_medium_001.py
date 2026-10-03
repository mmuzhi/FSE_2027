from typing import List
from collections import defaultdict, deque

class Solution:
    def findAllRecipes(self, recipes: List[str], ingredients: List[List[str]], supplies: List[str]) -> List[str]:
        graph = defaultdict(list)
        indegree = {}
        
        for i, recipe in enumerate(recipes):
            indegree[recipe] = len(ingredients[i])
            for ing in ingredients[i]:
                graph[ing].append(recipe)
        
        queue = deque(supplies)
        recipe_set = set(recipes)
        result = []
        
        while queue:
            item = queue.popleft()
            if item in recipe_set:
                result.append(item)
            for dependent in graph[item]:
                indegree[dependent] -= 1
                if indegree[dependent] == 0:
                    queue.append(dependent)
        
        return result