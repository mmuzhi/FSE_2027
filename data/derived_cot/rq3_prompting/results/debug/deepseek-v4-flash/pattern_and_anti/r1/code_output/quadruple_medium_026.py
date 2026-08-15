from typing import List
from collections import defaultdict

class Solution:
    def findAllRecipes(self, recipes: List[str], ingredients: List[List[str]], supplies: List[str]) -> List[str]:
        dct = defaultdict(list)
        indegree = {}
        n = len(recipes)

        for recipe in recipes:
            indegree[recipe] = 0

        for ing_list in ingredients:
            for ing in ing_list:
                indegree[ing] = 0

        for i in range(n):
            if recipes[i] in supplies:
                continue
            for ing in ingredients[i]:
                dct[ing].append(recipes[i])
                indegree[recipes[i]] += 1

        st = []
        for node in indegree:
            if indegree[node] == 0:
                st.append(node)

        flst = []
        ans = defaultdict(list)

        while st:
            x = st.pop(0)

            for recipe in dct[x]:
                for pre in ans[x]:
                    if pre not in ans[recipe]:
                        ans[recipe].append(pre)
                ans[recipe].append(x)
                indegree[recipe] -= 1
                if indegree[recipe] == 0:
                    st.append(recipe)

            if x in recipes:
                for pre in ans[x]:
                    if pre not in supplies:
                        break
                else:
                    flst.append(x)
                    if x not in supplies:
                        supplies.append(x)

        return flst