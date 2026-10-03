class Solution:
    def findRestaurant(self, list1: List[str], list2: List[str]) -> List[str]:
        d2 = {}
        for i in range(len(list2)):
            d2[list2[i]] = i
        
        l = []
        for i in range(len(list1)):
            if list1[i] in d2:
                l.append([i + d2[list1[i]], list1[i]])
        
        if not l:
            return []
        
        l.sort(key=lambda x: x[0])  # Sort by the first element (the sum)
        
        l1 = [l[0][1]]
        for i in range(1, len(l)):
            if l[i][0] == l[i-1][0]:
                l1.append(l[i][1])
            else:
                break
        
        return l1