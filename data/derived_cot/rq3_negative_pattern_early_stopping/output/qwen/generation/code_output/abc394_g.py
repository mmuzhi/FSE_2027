import sys
from collections import deque
from heapq import heappush, heappop

def main():
    data = sys.stdin.read().split()
    it = iter(data)
    H = int(next(it)); W = int(next(it))
    F = []
    for _ in range(H):
        row = [int(next(it)) for _ in range(W)]
        F.append(row)
    
    Q = int(next(it))
    queries = []
    for _ in range(Q):
        a = int(next(it)); b = int(next(it)); y = int(next(it))
        c = int(next(it)); d = int(next(it)); z = int(next(it))
        queries.append((a, b, y, c, d, z))
    
    # We are going to precompute the minimum stairs required for each building to reach the target building?
    # But note: the queries are independent and the target floor and building vary.
    # We need to answer each query separately.

    # However, note that the constraints: H, W up to 500, and Q up to 200000.
    # We cannot iterate over all floors.

    # Another idea: we can use a BFS-like approach but on the grid of buildings, but the state is (i, j, floor) which is too big.

    # Let me think: the total stairs is the sum of the absolute differences in each building. 
    # But note: we can break the journey arbitrarily. The key is that we can use walkways to move between buildings at the same floor, and then adjust the floor in the new building.

    # The problem is similar to: we have a graph where each node is a building, and we can move from one building to an adjacent building at the same floor (if the adjacent building has at least that floor). Then, we can adjust the floor in the current building arbitrarily (paying the absolute difference). 

    # We want to go from (A, B, Y) to (C, D, Z). 

    # We can consider that the entire journey is a sequence of buildings. Let the buildings be (i1, j1), (i2, j2), ... (ik, jk) with (i1, j1) = (A, B) and (ik, jk) = (C, D). Then, the total stairs is the sum of |x1 - x2| (for the first building's floor to the second building's floor) plus |x2 - x3| + ... but wait, no: in the first building, we start at Y and then go to x1 (if we change) and then use walkway to the next building at floor x1, then in the next building we change from x1 to x2 (paying |x1 - x2|), etc.

    # Actually, the stairs are used in each building independently. The total stairs is the sum of the absolute differences of the floor changes in each building. 

    # But note: we can also use stairs to go from the start floor to a floor that is not the same as the next building's floor. 

    # The problem is: we want to minimize the total stairs. 

    # Let me define a function f(i, j, x) = minimum total stairs to reach building (i, j) at floor x. But x can be up to 10^6, so we cannot store that.

    # We need to find a way to reduce the state space.

    # Observation: the only floors that matter are the ones that are the minimum of the building's floors along the path? Or the floors that are the starting floor, target floor, and the floors that are the boundaries (like the minimum of the two buildings' floors when switching).

    # Actually, we can use a Dijkstra-like algorithm on the grid of buildings, but the state is (i, j) and we store the minimum total stairs to reach (i, j) at a floor that is "compatible" with the target. But wait, the floor matters for the condition of walkways.

    # Alternatively, we can consider that the total stairs is the sum of the absolute differences of the floors we choose in each building. 

    # But note: we can also use the fact that we can change the floor arbitrarily in a building. So the minimal stairs for a building is the absolute difference between the floor we entered and the floor we leave (if we leave by walkway) or the floor we end at (if we end in that building). 

    # However, we can also stay in a building and adjust the floor multiple times. But the minimal stairs to change from floor a to floor b in a building is |a - b|.

    # So the problem is: we have a graph where each node is a building, and we can move from one building to an adjacent