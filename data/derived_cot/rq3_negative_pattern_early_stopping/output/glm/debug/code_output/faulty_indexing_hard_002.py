class Solution:
    def findMaximumElegance(self, items: List[List[int]], k: int) -> int:
        items.sort(key=lambda x: x[0], reverse=True)
        total_profit = 0
        seen = set()
        duplicate_profits = []
        
        for i in range(k):
            profit, category = items[i]
            total_profit += profit
            if category in seen:
                duplicate_profits.append(profit)
            else:
                seen.add(category)
        
        duplicate_profits.sort(reverse=True)
        distinct_count = len(seen)
        max_elegance = total_profit + distinct_count ** 2
        
        for i in range(k, len(items)):
            profit, category = items[i]
            if category not in seen and duplicate_profits:
                min_dup = duplicate_profits.pop()
                total_profit = total_profit - min_dup + profit
                seen.add(category)
                distinct_count += 1
                max_elegance = max(max_elegance, total_profit + distinct_count ** 2)
                
        return max_elegance