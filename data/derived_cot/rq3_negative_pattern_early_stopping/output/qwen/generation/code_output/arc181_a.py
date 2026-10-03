import sys

def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    index = 1
    answers = []
    for _ in range(t):
        n = int(data[index]); index += 1
        p = list(map(int, data[index:index+n]))
        index += n
        
        # If the permutation is already identity, answer 0.
        if p == list(range(1, n+1)):
            answers.append("0")
            continue
            
        # We are going to consider the following:
        # Operation k leaves the k-th element (1-indexed) unchanged. 
        # We can use operations to fix the array. The minimum number of operations is the minimum number of k's we need to choose so that:
        #   - Each operation k leaves the k-th element unchanged (so if we do an operation k, then the k-th element must be k at the time of the operation) and then the two parts are sorted.
        #
        # However, note that the operation k does not require the k-th element to be k at the time of the operation? Actually, it leaves the k-th element (whatever it is) at the k-th position. But then we require that at the end, the k-th element is k. So if we do an operation k, then the k-th element must become k at some point. But note: the operation k leaves the k-th element unchanged, so if the k-th element is not k at the time of the operation, then after the operation it is still not k. Therefore, we must have the k-th element equal to k at the time of the operation.
        #
        # Therefore, the operation k can only be done when the k-th element is k. Otherwise, it leaves an incorrect element at the k-th position.
        #
        # So the operations must be done in an order such that when we do an operation k, the k-th element is k (so that it remains k) and then we sort the two parts. But note: the two parts might contain the correct elements or not. However, the operation k will sort the two parts, so if the two parts are not sorted, then the operation k will fix them (if they are not sorted) but might break the identity of other elements? Actually, no: the operation k only leaves the k-th element and sorts the two parts. The elements in the two parts are moved arbitrarily (to sorted order) but the k-th element is fixed. 
        #
        # Now, note: the operation k does not necessarily fix the entire array. It might fix the two parts but leave other elements incorrect. 
        #
        # We need to find the minimum number of operations to fix the entire array.
        #
        # Observation: 
        #   Operation k can fix the entire array if the entire array is already sorted except that the k-th element is k and the two parts are not sorted. Then one operation k will sort the two parts and leave k at k, so the entire array becomes identity.
        #
        # But note: the operation k does not require the two parts to be sorted. It will sort them. So if the two parts are not sorted, then the operation k will fix them. However, if the two parts are already sorted, then the operation k does nothing to the two parts (since sorting a sorted array is the same) and leaves the k-th element, so the array remains the same. Therefore, the operation k is only useful if the two parts are not sorted.
        #
        # However, we can use multiple operations. The idea is that we can fix the array by fixing the positions one by one. But note: the operation k fixes the k-th position and sorts the two parts. But the two parts might contain the correct elements for their positions? Not necessarily.
        #
        # Another observation: 
        #   The operation k leaves the k-th element and sorts the two parts. Therefore, the operation k can be seen as: 
        #       We are allowed to fix the k-th element (if it is correct) and then we can sort the rest arbitrarily (but note: the rest is split into two parts and sorted independently). 
        #
        # But note: the operation k does not fix the entire array. It only fixes the k-th element (if it was correct) and sorts the two parts. However, if the two parts are not sorted, then the operation k will fix them. But if the two parts are sorted, then the operation k does nothing (except leave the k-th element). 
        #
        # Therefore, the operation k is only useful if the two parts are not sorted. And note: the two parts must be sorted for the entire array to be identity. 
        #
        # Now, consider: what is the minimum number of operations?
        #
        # We can consider that an operation k fixes the k-th