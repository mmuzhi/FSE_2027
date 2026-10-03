from collections import deque
from typing import List
from collections import defaultdict

class Solution:
    def findAllRecipes(self, recipes: List[str], ingredients: List[List[str]], supplies: List[str]) -> List[str]:
        graph_recipe = {}
        for i in range(len(recipes)):
            graph_recipe[recipes[i]] = ingredients[i]
        
        graph_ingredient_to_recipe = defaultdict(list)
        for recipe, ings in graph_recipe.items():
            for ing in ings:
                graph_ingredient_to_recipe[ing].append(recipe)
        
        available = set(supplies)
        made = set()
        q = deque(supplies)
        
        while q:
            u = q.popleft()
            if u in graph_ingredient_to_recipe:
                for recipe in graph_ingredient_to_recipe[u]:
                    can_make = True
                    for ing in graph_recipe[recipe]:
                        if ing not in available:
                            can_make = False
                            break
                    if can_make and recipe not in made:
                        made.add(recipe)
                        available.add(recipe)
                        q.append(recipe)
        
        return list(made)