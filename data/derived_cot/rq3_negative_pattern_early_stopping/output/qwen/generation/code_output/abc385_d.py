import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    
    # Parse the first four integers: N, M, S_x, S_y
    it = iter(data)
    N = int(next(it)); M = int(next(it)); S_x = int(next(it)); S_y = int(next(it))
    
    # Read N houses
    houses = []
    for _ in range(N):
        x = int(next(it)); y = int(next(it))
        houses.append((x, y))
    
    # Read M moves
    moves = []
    for _ in range(M):
        d = next(it)
        c = int(next(it))
        moves.append((d, c))
    
    # We'll simulate the journey and record the set of houses visited.
    # But we cannot check every house for every move (too slow). Instead, we can check for each house if it lies on any of the moves.

    # However, note: The journey is a sequence of line segments. We can check for each house if it lies on any of the segments.

    # But the number of houses is up to 200,000 and moves up to 200,000, so we cannot check each house against each move (200,000 * 200,000 is 40e9, too many).

    # Alternative: We can check each move against the set of houses. But then we have to check for each move and each house? Still too slow.

    # We need a better idea.

    # Let's think: The journey is a polygonal chain. We are only interested in the houses (points) that lie on the chain.

    # We can do:

    #   Start at (S_x, S_y) and then for each move, we have a segment from (x, y) to (x', y').

    #   For a horizontal move (L or R): the segment is from (x, y) to (x ± C, y). We can check if any house (a, b) has b == y and a between min(x, x±C) and max(x, x±C) (inclusive).

    #   Similarly for vertical.

    # But then we have to check for each house and each move? That's O(N*M) which is too slow.

    # We need to invert the problem: For each move, we want to know which houses (from the given set) lie on that segment.

    # However, the houses are fixed and the segments are axis-aligned. We can use a sweep-line and segment trees? But that might be too heavy.

    # Another idea: Precompute a set of houses. Then, for each move, we can check the houses that lie on the segment by:

    #   For horizontal move: 
    #       condition: y == house_y and house_x between the two x-coordinates of the segment.
    #   Similarly for vertical.

    # But then we have to check all houses for each move. That's 200,000 * 200,000 = 40e9 checks, which is too slow in Python.

    # We need to optimize.

    # Idea: Precompute two dictionaries (or sets) for houses by their x and y coordinates? But then how?

    # Alternatively, we can use the fact that the moves are axis-aligned and the houses are fixed. We can precompute:

    #   Horizontal houses: group houses by y-coordinate. Then for a horizontal move at y, we look at all houses with that y, and then check if their x is between the segment's x-range.

    #   Similarly, for vertical moves: group houses by x-coordinate.

    # Steps:

    #   Precompute:
    #       horizontal_house_by_y = defaultdict(list)
    #       vertical_house_by_x = defaultdict(list)

    #   Then, for each move:
    #       If it's horizontal (L or R): 
    #           y = current y (which is the y of the starting point of the move)
    #           Then, look up all houses in horizontal_house_by_y[y] and check if their x is between the segment's x-range (from the starting x to the ending x, inclusive).
    #       Similarly for vertical.

    #   But note: the same house might be encountered multiple times, but we only want to count it once. So we can use a set for visited houses.

    #   However, we must be cautious: The journey is continuous and the house might be passed multiple times, but we count it only once.

    #   But the problem: The houses are distinct and the journey is a straight line. So if a house is on the segment, it is either passed once or not at all.

    #