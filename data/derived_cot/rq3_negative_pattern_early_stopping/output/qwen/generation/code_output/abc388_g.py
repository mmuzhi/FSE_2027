import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1+n]))
    q = int(data[1+n])
    queries = []
    index = 1+n+1
    for i in range(q):
        L = int(data[index]); R = int(data[index+1]); index += 2
        queries.append((L, R))
    
    # Precompute the answers for each query? But note: the array is sorted, and queries are arbitrary segments.
    # We cannot precompute for all segments because there are too many.

    # Instead, we can use a two-pointer method on the entire array and then use a segment tree or something? 
    # But note: the constraints are up to 200,000 for N and Q.

    # Alternate approach: 
    # We note that the condition for a pair (a, b) is a <= b/2. This is equivalent to b >= 2*a.
    # We can try to use a greedy matching from the largest to the smallest.

    # However, note that the array is sorted. We can consider: 
    #   Let the segment be A[L-1:R] (0-indexed). We want to form as many pairs as possible.

    # We can use a two-pointer method that starts from the beginning and the end, but we must be careful.

    # Actually, we can use a greedy matching that goes from the largest to the smallest, and for each large number, we try to find the smallest number that is <= half of it. But then we remove that small number.

    # But note: the condition is a <= b/2, so for a fixed b, we need a <= b/2. The smallest a that satisfies the condition is the smallest number in the segment, but we cannot use the same a twice.

    # We can do:
    #   Sort the segment (but the entire array is sorted, so the segment is sorted).
    #   Then, we can use two pointers: one at the beginning (left) and one at the end (right). We want to count the number of pairs.

    # However, note: the condition is not symmetric. We can also consider: 
    #   We want to use the smallest numbers as the small ones and the largest numbers as the large ones. But the condition is that the small one must be <= half of the large one.

    # We can use a two-pointer method that traverses from the largest to the smallest and for each large number, we try to find a small number that is <= half of it. But we must use each small number only once.

    # Actually, we can use a greedy matching from the smallest to the largest? 

    # Let's try: 
    #   We'll traverse from the largest to the smallest, and for each large number, we look for a small number that is <= half of it. But we want to use the smallest available small number that is <= half of the large number, because if we use a larger small number, then we might block a pair for a smaller large number.

    # However, note: the condition is a <= b/2. For a fixed b, the condition is independent of other pairs. But we want to maximize the number of pairs.

    # We can use a two-pointer method that starts from the beginning (for small numbers) and the end (for large numbers). But the condition is: for a given small number a, we can pair it with any large number b such that b >= 2*a.

    # We can do:
    #   Let left = 0, right = m-1 (for the segment)
    #   We want to count the pairs.

    # But note: the condition is not about consecutive elements. 

    # Alternate known approach for similar problems (like two-sum or matching with condition) is to use two pointers and move the pointers appropriately.

    # We can try: 
    #   We want to form as many pairs as possible. Each pair requires one small and one large. The condition is that the small must be <= half the large.

    # We can use a greedy: 
    #   Sort the segment (already sorted).
    #   Then, we can use two pointers: one at the beginning (for small) and one at the end (for large). But we need to assign small numbers to large numbers.

    # Actually, we can use a two-pointer method that counts the number of pairs by matching the smallest available number with the largest available number that is at least twice the smallest. Then remove both and continue.

    # Steps for a segment (sorted):
    #   Let left = 0, right = m-1, count = 0.
    #   While left < right:
    #       If A