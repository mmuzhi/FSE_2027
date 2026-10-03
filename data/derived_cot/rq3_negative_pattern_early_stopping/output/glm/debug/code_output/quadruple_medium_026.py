from typing import List
from collections import defaultdict, deque

class Solution:
    def findAllRecipes(self, recipes: List[str], ingredients: List[List[str]], supplies: List[str]) -> List[str]:
        dct = defaultdict(list)
        indegree = defaultdict(int)
        n = len(recipes)
        recipes_set = set(recipes)
        
        for i in range(n):
            for j in ingredients[i]:
                dct[j].append(recipes[i])
                indegree[recipes[i]] += 1
                
        st = deque(supplies)
        flst = []
        
        while st:
            x = st.popleft()
            if x in recipes_set:
                flst.append(x)
            for i in dct[x]:
                indegree[i] -= 1
                if indegree[i] == 0:
                    st.append(i)
                    
        return flst