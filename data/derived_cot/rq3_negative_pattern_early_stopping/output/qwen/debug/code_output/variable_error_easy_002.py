class Solution:
    def findRestaurant(self, list1: List[str], list2: List[str]) -> List[str]:
        d2 = {}
        for i in range(len(list2)):
            d2[list2[i]] = i
        
        common = []
        for i in range(len(list1)):
            if list1[i] in d2:
                common.append([i + d2[list1[i]], list1[i]])
        
        if not common:
            return []
        
        common.sort(key=lambda x: x[0])
        
        min_sum = common[0][0]
        result = []
        for i in range(len(common)):
            if common[i][0] == min_sum:
                result.append(common[i][1])
            else:
                break
        
        return result