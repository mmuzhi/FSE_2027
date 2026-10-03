import sys
from collections import deque

def main():
    data = sys.stdin.read().split()
    it = iter(data)
    n = int(next(it))
    W = [int(next(it)) for _ in range(n)]
    intervals = []
    for _ in range(n):
        L = int(next(it))
        R = int(next(it))
        intervals.append((L, R))
    
    q = int(next(it))
    queries = []
    for _ in range(q):
        s = int(next(it))
        t = int(next(it))
        queries.append((s, t))
    
    # Build a graph where edges are between non-overlapping intervals.
    # But building the graph directly is O(n^2). We need to use an interval tree or something similar.

    # Alternatively, we can think of the graph as the complement of the interval overlap graph.
    # But note: the graph is defined by non-overlapping intervals. We can use a technique to build a graph of non-overlapping intervals by considering the ordering of intervals.

    # Idea: sort intervals by their left endpoints. Then, two intervals do not overlap if the next interval's left is greater than the current interval's right.

    # But how to build the graph without O(n^2) edges?

    # Another idea: use a union-find or BFS on intervals? But the graph is huge.

    # Alternatively, we can use a technique to connect intervals that are non-overlapping by using a sweep line and a segment tree or a priority queue.

    # However, note that the graph is defined by non-overlapping intervals. This is the same as the graph where two intervals are connected if they are disjoint.

    # We can use the following approach:

    # 1. Sort the intervals by their left endpoints.
    # 2. Then, for each interval, we can find the next interval that starts after the current interval ends (non-overlapping). But that would be O(n) per interval, which is O(n^2) overall.

    # We need a more efficient way.

    # Another idea: use a graph where we connect intervals that are disjoint by using a "time-line" and then connect intervals that are separated by gaps. But how?

    # Alternatively, we can use a technique from "interval graphs" but in the complement. The complement of an interval graph is not necessarily an interval graph, but we can use the following:

    # We can build a graph where edges are between intervals that are disjoint by using a two-pass method:

    # - Sort intervals by left endpoints.
    # - Then, for each interval, we can find the first interval that starts after the current interval ends. Then, we can connect the current interval to all intervals that start after the current interval ends? But that would be too many.

    # But note: the graph is defined by non-overlapping intervals. We can use a "gap" method: intervals that are disjoint can be connected if they are separated by a gap. But how to build the graph without enumerating all edges?

    # We can use a technique to build a graph of intervals by considering the following:

    # - Sort intervals by left endpoints.
    # - Then, for each interval, we can find the next interval that starts after the current interval ends. Then, we can connect the current interval to that interval and beyond? But then, we need to connect to all intervals that are disjoint? That's too many.

    # Alternatively, we can use a "two-layer" graph: one layer for intervals and another for gaps? Or use a line graph?

    # Another idea: use a "virtual node" for each gap. But the gaps are between intervals.

    # Actually, we can use a method similar to building a graph for interval scheduling. But we need to connect intervals that are disjoint.

    # Let me think differently: the graph is the complement of the interval overlap graph. The interval overlap graph has edges between intervals that overlap. The complement graph has edges between intervals that do not overlap.

    # We can use the following: the graph is the complement of an interval graph. The complement of an interval graph is a circular arc graph, but that might not help.

    # Alternatively, we can use a technique to build a graph of intervals by considering the following:

    # - Sort intervals by their left endpoints.
    # - Then, for each interval, we can find the next interval that starts after the current interval ends. Then, we can connect the current interval to all intervals that start after the current interval ends? But that would be too many.

    # But note: the graph is defined by non-overlapping intervals. We can use a "two-pointer" method to connect intervals that are disjoint by their positions.

    # However, the problem is that the graph is huge. We need to avoid building the graph explicitly.

    # We need to answer connectivity and minimum weight path queries. This suggests that we need