class ArrangementCalculator:
    def __init__(self, datas):
        self.datas = list(datas)
    
    @staticmethod
    def count(n, m=-1):
        if m == -1 or n == m:
            return ArrangementCalculator.factorial(n)
        else:
            return ArrangementCalculator.factorial(n) // ArrangementCalculator.factorial(n - m)
    
    @staticmethod
    def count_all(n):
        total = 0
        for i in range(1, n + 1):
            total += ArrangementCalculator.count(n, i)
        return total
    
    @staticmethod
    def factorial(n):
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

    def select(self, m=-1):
        if m == -1:
            m = len(self.datas)
        
        result = []
        if m == 0:
            return [self.datas[:0]]  # Return empty list if m is 0
        
        current = []
        remaining = self.datas[:]
        self.permutations_recursive(current, remaining, m, result)
        return result

    def select_all(self):
        result = []
        n = len(self.datas)
        for i in range(1, n + 1):
            partial_result = self.select(i)
            result.extend(partial_result)
        return result

    def permutations_recursive(self, current, remaining, m, result):
        if len(current) == m:
            result.append(current[:])
            return
        
        for i in range(len(remaining)):
            new_current = current + [remaining[i]]
            new_remaining = remaining[:i] + remaining[i+1:]
            self.permutations_recursive(new_current, new_remaining, m, result)