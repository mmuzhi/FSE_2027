class Solution:
    def findAllRecipes(self, recipes: List[str], ingredients: List[List[str]], supplies: List[str]) -> List[str]:
        dct = defaultdict(list)
        indegree = {}
        n = len(recipes)
        supplies_set = set(supplies)

        for i in range(n):
            indegree[recipes[i]] = 0
            for j in ingredients[i]:
                if j not in supplies_set:
                    dct[j].append(recipes[i])
                    indegree[recipes[i]] += 1

        st = []
        for i in indegree:
            if indegree[i] == 0:
                st.append(i)

        result = []
        while st:
            x = st.pop()
            result.append(x)
            for i in dct[x]:
                indegree[i] -= 1
                if indegree[i] == 0:
                    st.append(i)

        return result