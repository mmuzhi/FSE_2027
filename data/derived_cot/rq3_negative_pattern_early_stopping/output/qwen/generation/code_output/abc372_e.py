import heapq
import sys

def main():
    data = sys.stdin.read().split()
    it = iter(data)
    n = int(next(it)); q = int(next(it))
    
    # We'll create an array (list) for each vertex from 1 to n.
    # Each element is a min-heap (for the largest neighbors) but we want to keep the largest 10.
    # We'll store the heap for each vertex. But note: we are only asked for the k-th largest, and k is at most 10.
    # We'll use a list of heaps (min-heaps) for each vertex. But we want the largest 10, so we store the 10 largest in a min-heap.
    # However, we want to be able to get the k-th largest. We can store the 10 largest (or less) in a min-heap, then to get the k-th largest, we can sort the heap in descending order and pick the (k-1)-th element.

    # But note: the graph is undirected. We have to update both u and v.

    # We'll create a list `graph` of size n+1 (index from 1 to n). Each element is a min-heap (for the largest neighbors) but we want to keep the largest 10. However, we can also use a list of lists and then use heapq to maintain the min-heap for the largest 10.

    # Alternatively, we can use a list of lists and then use heapq.nlargest(10, list) but that is O(n) and n can be large. But we are only storing up to 10, so we can do:

    # We'll maintain for each vertex a min-heap (for the largest 10) and also we need to avoid duplicates? Actually, each edge is added once, and we are adding the same edge twice (for u and v). But note: the graph is undirected, so when we add edge (u, v), we add v to u's list and u to v's list.

    # However, we must avoid adding the same neighbor multiple times? Actually, the input says "1 u v" and u < v, so no duplicate edges. But note: the graph is undirected, so we are adding both directions.

    # We'll create an array `neighbors` of size n+1 (index 0 unused). Each element is a min-heap (for the largest 10 neighbors). But note: we want the largest 10, so we can push the neighbor and then if the heap size exceeds 10, pop the smallest.

    # However, we must be cautious: we are storing the largest 10. So we want to keep the 10 largest. We can do:

    # For a vertex v, when we add a neighbor u, we push u to the heap. Then if the heap has more than 10, we pop the smallest.

    # But note: the same neighbor might be added multiple times? No, because edges are unique.

    # Steps for adding an edge (u, v):
    #   For vertex u: push v to the heap. Then if len(heap) > 10, pop the smallest.
    #   For vertex v: push u to the heap. Then if len(heap) > 10, pop the smallest.

    # Then for a query (2 v k):
    #   Let h = neighbors[v]
    #   If the heap has less than k elements, output -1.
    #   Else, we want the k-th largest. We can get the k-th largest by taking the k-th largest from the heap. But note: the heap is a min-heap of the largest 10. The k-th largest is the (k-1)-th element in the sorted list (descending) of the heap.

    # But note: the heap is a min-heap, so the smallest element is at the top. We can get the k-th largest by:

    #   Let sorted_list = sorted(h, reverse=True)   # This gives descending order: [max, ..., min]
    #   Then the k-th largest is sorted_list[k-1] (if k <= len(h))

    # However, we can also use nlargest(k, h) which returns the k largest in descending order. Then the first element is the largest, the second is the second largest, etc.

    # But note: we are storing the largest 10, so we can use heapq.nlargest(k, h) to get the k largest. Then the k-th largest is the last element of the list returned by nlargest(k, h)? No, the nlargest(k, h) returns the k largest in descending order. So the first element is the largest