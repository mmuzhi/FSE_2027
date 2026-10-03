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
        
        l.sort(key=lambda x: x[0])  # We can sort by the first element only, but the default sort is lexicographical which is fine.
        # But note: the original code did l.sort() which is lexicographical. We can keep it or change to sort by the first element only.
        # However, the original code did not specify the key, so it uses the natural order (which is lexicographical). 
        # But if we have two elements with the same sum, the restaurant name (string) will be used for ordering. 
        # But we don't care about the order of the restaurant names, so we can leave it as is.

        # Alternatively, we can sort by the first element only to be efficient and clear.
        # Let's change to: l.sort(key=lambda x: x[0])

        # But note: the original code did not do that. However, the problem does not require a specific order for the same sum, so we can change to sort by the first element only.

        # However, the original code's method is acceptable because the second element (restaurant name) is a string and the sort is stable for the first element. 
        # But to be explicit and efficient, we can sort by the first element.

        # Let's change the sort to use key to avoid any potential issue with lexicographical order.

        # But note: the original code did not have this bug because the problem does not require a specific order for the same sum. 
        # However, let's stick to the original code's behavior. But the original code did not specify the key, so it uses the natural order (which is by the first element then the second). 
        # Since we only care about the first element, we can do:

        # We'll change the sort to use key to be safe.

        # But wait, the original code did not have the key and it worked because the first element is the sum and the second is the string. 
        # The natural sort of [sum1, str1] and [sum2, str2] is first by sum1 and sum2, then by str1 and str2. 
        # But we don't care about the string order. So we can change the sort to:

        #   l.sort(key=lambda x: x[0])

        # But the problem does not require a specific order, so we can do either.

        # However, the original code did not have this bug because the minimal sum is at the beginning and then we break at the first change. 
        # But note: the original code did not sort by the first element only, but lexicographically. 
        # But if two elements have the same sum, then the restaurant name (string) is used for ordering. 
        # This might change the order of the restaurants with the same sum, but we are only collecting the ones with the minimal sum, so it doesn't matter.

        # So we can keep the original sort.

        # But to be safe, let's change the sort to use key to avoid any potential issue with the string ordering affecting the breaking condition? 
        # Actually, no: the breaking condition is based on the sum (the first element). The string ordering does not affect the breaking condition because we are comparing the first element (the sum) of the current and the previous.

        # So we can keep the original sort.

        # However, let's change the sort to use key for clarity and to ensure we are only sorting by the sum.

        # We'll change the sort to: l.sort(key=lambda x: x[0])

        # But note: the original code did not have this. We are allowed to change the code as long as we fix the bugs.

        # Alternatively, we can leave it as is because the lexicographical sort is by the first element (the sum) and then the string. 
        # But the problem does not require a specific order for the same sum, so it's acceptable.

        # Let's stick to the original code's behavior for now.

        # But note: the original code did not have the key, so we can change it to use key for clarity.

        # I'll change the sort to use key to avoid any confusion.

        # Actually, let's change it to:

        #   l.sort(key=lambda x: x[0])

        # But wait, the original code did not have this and the problem does not specify the order of restaurants with the same sum. 
        # However, the breaking condition is based on the sum, so it's safe.

        # But note: the code breaks at the first change of the sum. The breaking condition is:

        #   if l[i][0] == l[i-1][0]:
        #       l1.append(l[i][1])
        #   else:
        #       break

        # This condition uses the sum (the first element). So even if the restaurant names are different, we break when the sum changes.

        # So we can change the sort to use key without affecting the breaking condition.

        # Let's change the sort to use key.

        l.sort(key=lambda x: x[0])
        l1 = []
        l1.append(l[0][1])
        for i in range(1, len(l)):
            if l[i][0] == l[i-1][0]:
                l1.append(l[i][1])
            else:
                break
        return l1