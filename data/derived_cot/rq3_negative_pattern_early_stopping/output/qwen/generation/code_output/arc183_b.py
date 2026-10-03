import sys

def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    index = 1
    results = []
    for _ in range(t):
        n = int(data[index]); index += 1
        k = int(data[index]); index += 1
        # Read array A of n integers
        a = list(map(int, data[index:index+n])); index += n
        # Read array B of n integers
        b = list(map(int, data[index:index+n])); index += n
        
        # Condition 1: For each index i, the value b[i] must appear in the array a at least once.
        # But note: we are allowed to change any index arbitrarily (because the graph is connected) so we can change any index to any value that is present in the entire array.
        # However, we must check that for every i, b[i] is in the set of values that appear in a.
        # But note: what if the value b[i] is not in a? Then we cannot change any index to b[i] because we don't have that value in the array to copy from.
        # So we can do:
        #   Let S = set(a)
        #   For each i, if b[i] not in S, then we break and say No.
        # However, note: the problem constraints say that the total N across test cases is at most 250000, so we can do this.

        # But wait: what if the graph is not connected? Actually, the graph is connected for K>=1 (since K>=1 and K < N, and N>=2). So we can change any index to any value that is in the entire array.

        # However, there is a nuance: we are allowed to change an index i to a value that is present in the array, but we must have that value somewhere. And we can use the entire array to copy from.

        # But note: the operations are defined as: choose i and j (with |i-j|<=K) and set A_i = A_j. We can do this repeatedly. So we can change any index to any value that is present in the array.

        # Therefore, the condition is: for every index i, the value b[i] must be present in the array a.

        # However, wait: what if the value b[i] is present in a, but we cannot reach the index j that has b[i] from i? But the graph is connected, so we can.

        # But note: the graph is connected, so we can change any index to any value that is present in the array.

        # Therefore, we just need to check that for every i, b[i] is in the set of values of a.

        # However, consider: what if the value b[i] is present in a, but we are not allowed to change an index i to a value that is not in the original a? Actually, we are allowed to change arbitrarily because we can copy from any index that has the value. And we can change multiple indices arbitrarily.

        # But note: the operations do not require that the value we are copying from remains unchanged? Actually, we can change an index multiple times. So we can change an index i to a value that is present in a, and then use that changed index to change others.

        # However, the condition is: we can change A_i to A_j (the current value of A_j). So if we change an index j first, then we can use that changed value to change others.

        # But note: the problem does not require that we preserve the original array. We can change arbitrarily.

        # Therefore, the necessary and sufficient condition is that for every i, the value b[i] must be present in the array a (at least once) at the beginning? Actually, no: because we can change the array arbitrarily, we can change an index j to have the value b[i] even if originally a[j] was not b[i]. But wait, we can only copy from an index that has the value we want at the time of copying.

        # However, we can do multiple operations. For example, to set an index i to a value x that is not originally in a at index i, but is present elsewhere, we can copy from an index j that has x. But note: if x is not in the original a, then we cannot get it. So the condition is that for every i, b[i] must be in the set of values that appear in the original a.

        # But wait: what if we need to change an index i to a value x, and x is not in the original a? Then we cannot. So condition: for every i, b[i] must be in the set of original a.

        # However, consider: