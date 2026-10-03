class Solution:
    def maxAmount(self, initialCurrency: str, pairs1: List[List[str]], rates1: List[float], pairs2: List[List[str]], rates2: List[float]) -> float:
        # Build graph for day1
        graph1 = {}
        # Add nodes
        currencies = set()
        currencies.add(initialCurrency)
        for i in range(len(pairs1)):
            a, b = pairs1[i]
            currencies.add(a)
            currencies.add(b)
        for i in range(len(pairs1)):
            a, b = pairs1[i]
            r = rates1[i]
            # Add edge a->b with rate r
            if a not in graph1:
                graph1[a] = []
            graph1[a].append((b, r))
            # Add reverse edge b->a with rate 1/r
            if b not in graph1:
                graph1[b] = []
            graph1[b].append((a, 1/r))
        
        # Build graph for day2
        graph2 = {}
        for i in range(len(pairs2)):
            a, b = pairs2[i]
            r = rates2[i]
            if a not in graph2:
                graph2[a] = []
            graph2[a].append((b, r))
            if b not in graph2:
                graph2[b] = []
            graph2[b].append((a, 1/r))
        
        # For day1: compute dp1[node] = maximum amount of node obtainable from initialCurrency
        dp1 = {node: 0.0 for node in currencies}
        dp1[initialCurrency] = 1.0
        
        # Relaxation for day1
        changed = True
        while changed:
            changed = False
            for node in graph1:
                if dp1[node] == 0.0:
                    continue
                for neighbor, rate in graph1[node]:
                    new_amount = dp1[node] * rate
                    if new_amount > dp1[neighbor]:
                        dp1[neighbor] = new_amount
                        changed = True
        
        # For day2: compute g[node] = maximum amount of initialCurrency obtainable from node
        g = {node: 0.0 for node in currencies}
        # If we start at initialCurrency, we can have 1.0
        g[initialCurrency] = 1.0
        
        # But note: we might get more by converting away and coming back? 
        # Actually, we need to relax until no improvement
        changed = True
        while changed:
            changed = False