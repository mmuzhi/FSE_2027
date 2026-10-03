def main():
    import sys
    data = sys.stdin.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1+n]))
    
    total_moves = sum(A)
    # The minimal moves to complete S is n, so the remaining moves (total_moves - n) are "extra" moves that don't add new indices.
    # But note: the game ends when S is complete, so the last move is the one that completes S (if we haven't completed S earlier, but we can't complete S earlier than n moves).

    # However, the players can choose to use extra moves to their advantage. The key is that the player who makes the move that completes S wins.

    # But note: the set S is completed at the move that adds the last index. So the move that completes S is the one that adds the last index. However, if the last index was already added, then the move that completes S was the one that added the last index.

    # Actually, the game ends at the first move that makes S complete. So the total number of moves is not fixed. The players can control the order.

    # Alternate approach:

    # Consider that the game is equivalent to: we have n piles (each pile i has A_i tokens). On a move, a player can remove one token from any pile. Additionally, when a pile is reduced from a positive number to zero, we don't get any extra effect (except that the pile is "used" and cannot be used again to add to S). But note: the condition for adding an index to S is that the index is chosen and the value is at least 1 (so the first time you choose an index, you add it to S, and then subsequent choices don't add it). 

    # However, the game ends when all indices are in S, i.e., when each index has been chosen at least once.

    # This is similar to the game of Nim with a condition: the last move (the one that completes the set) wins.

    # But note: the moves are independent and the only constraint is that you cannot add an index more than once. The game is about collecting all indices (like a set cover) and the players can choose any index (any pile) to remove a token.

    # The total number of moves required to complete the set is at least n. The game ends at the move that completes the set.

    # How to determine the winner?

    # Let's denote:
    #   Let m = minimal moves to complete the set = n (if we choose each index exactly once, then we complete the set in n moves).
    #   But the players can choose to use more moves by repeatedly choosing the same index.

    # However, the players are playing optimally. The goal is to be the one who makes the last move (the one that completes the set).

    # The key is: the set S is completed when the last index is chosen for the first time. So the move that completes the set is the one that chooses the last index (if it hasn't been chosen before). But note: the set S is built by the first time an index is chosen.

    # Therefore, the game is equivalent to: we have n piles (each pile i has A_i tokens). A move consists of removing one token from any pile. The player who removes the last token from the last pile (i.e., the one that completes the set) wins? Not exactly.

    # Actually, the game ends when the set S is complete, which happens when each pile has been chosen at least once. But note: the set S is built by the first time an index is chosen. So the condition for the game to end is that we have chosen each index at least once. The total number of moves is the sum of the tokens, but the game ends at the move that completes the set.

    # However, the set S is completed at the move that adds the last index. So the move that completes the set is the one that chooses the last index for the first time. But note: the last index might be chosen multiple times, but the first time it is chosen is the move that completes the set.

    # Therefore, the game is equivalent to: we have n piles (each pile i has A_i tokens). On a move, a player removes one token from any pile. The player who removes the token that makes the set of piles that have been touched (i.e., have at least one token removed) complete (i.e., all n piles have been touched at least once) wins.

    # But note: the move that completes the set is the one that touches the last pile. However, the player might have already touched all piles, then the game ends at the move that completes the set (which is the move that touches the last pile). But if the game ends at the