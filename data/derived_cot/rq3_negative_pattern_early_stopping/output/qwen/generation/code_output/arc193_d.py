import sys

def main():
    data = sys.stdin.read().splitlines()
    t = int(data[0])
    index = 1
    results = []
    for _ in range(t):
        n = int(data[index]); index += 1
        A = data[index].strip(); index += 1
        B = data[index].strip(); index += 1
        
        # Check if there's any required square (B_i='1') that is not present in A at all.
        # But note: we can move pieces. However, the total number of pieces must be at least the number of required squares (since each required square must have at least one).
        # Also, the initial number of pieces is the count of '1's in A.
        # The required squares are the positions where B_i='1'. Let req_count = number of '1's in B.
        # If the initial number of pieces (count_A) is less than req_count, then it's impossible.
        count_A = A.count('1')
        count_B = B.count('1')
        if count_A < count_B:
            results.append("-1")
            continue
            
        # But even if count_A >= count_B, it might not be possible because of the movement constraints.
        # However, note that the problem constraints say that the total N over test cases is 10^6, so we can do an O(n) solution per test case.

        # Another observation: each operation moves all pieces toward a chosen center. This is similar to a voting system or median movement.

        # Let me think: what is the effect of an operation with center i?
        # Each piece at position j moves toward i by one. So, the net effect is that the entire set of pieces is shifted toward i.

        # We need to cover all required squares (where B_i='1') and avoid forbidden squares (B_i='0').

        # But note: the operations are simultaneous and all pieces move. So, the movement of each piece is determined by the sequence of centers chosen.

        # Alternatively, we can think of the problem as: we need to assign to each piece a sequence of moves (each move is a step toward a chosen center) such that after all moves, the piece ends up in one of the required squares (and the required squares are covered).

        # However, the operations are the same for all pieces. So, if we choose a center, all pieces move toward that center.

        # This is similar to a problem where you have to gather points by moving them toward a chosen center, but here we have to distribute the pieces to cover specific squares.

        # Another idea: consider the required squares (positions where B_i='1'). Let R be the set of required positions (1-indexed). 

        # Each piece must end up in one of the required squares. But note: the condition is that every required square must have at least one piece. So, we need to assign each required square at least one piece.

        # But the movement is constrained: each operation moves all pieces toward a chosen center. 

        # Observation: the movement of a piece from its initial position to a target position can be broken down into steps. However, the steps are not independent because all pieces move together.

        # Alternatively, consider the following: 

        # Let f(j) be the number of operations that have center >= j (for a piece starting at j). Similarly, let g(j) be the number of operations that have center <= j.

        # Then, the final position of a piece initially at j is: 
        #   j + (number of operations with center <= j) - (number of operations with center >= j)

        # But note: each operation moves the piece one step toward the center. So, if the center is to the left, the piece moves right; if to the right, the piece moves left.

        # Let x = number of operations with center <= j
        # Let y = number of operations with center >= j

        # Then, the piece moves right by y (because centers to the left of j will move it right) and left by x (because centers to the right of j will move it left). 

        # But wait, if the center is less than j, then the piece moves right (so +1 per operation with center < j). If the center is greater than j, then the piece moves left (so -1 per operation with center > j). 

        # So, the net movement is: (number of operations with center < j) - (number of operations with center > j)

        # Let total_operations = x + y + z, where z is the operations with center exactly j? But wait, if the center is j, then the piece doesn't move. 

        # Actually, we can define:
        #   Let L = number of operations with center <