def main():
    S = input().strip()
    T = input().strip()
    n = len(S)
    # If S is already T, then we output 0 and nothing else.
    if S == T:
        print(0)
        return

    # Count the number of differing positions
    diff = []
    for i in range(n):
        if S[i] != T[i]:
            diff.append(i)

    m = len(diff)
    # The minimum number of operations is m (each operation changes one differing character)
    # But note: we are allowed to change any character, and we can change a character that is not yet fixed? 
    # However, the goal is to have the lexicographically smallest sequence.

    # We have to change the differing characters in some order. But note: we can change a character that is not yet fixed to something else, and then fix it later.

    # However, the problem requires the minimum number of operations, so we must change each differing character exactly once.

    # But the order of changes matters for the lexicographical order of the entire sequence.

    # We have to produce a sequence of states (each state is a string) of length m (the number of operations). Each state is obtained by changing one character from the previous state.

    # The initial state is S (which is not appended). Then we do m operations, each operation changes one character and appends the new state.

    # We are free to choose which differing character to fix at each step, and what to change it to.

    # However, note: we must end at T. So the last operation must fix the last differing character to its target.

    # But we can change a character to an intermediate value and then change it again? That would require more operations. So we must fix each differing character exactly once.

    # However, consider: if we change a character to a value that is not T's value, then we have to change it again. But that would be two operations for one differing character, which is not minimal. So we must change each differing character to T's value exactly once.

    # But wait: what if we change a character to T's value and then change another character to T's value? Then the state after the first operation is: one differing character fixed, the rest still differ.

    # The challenge: we have to choose the order of fixing the differing characters and the intermediate values (if we fix one character, we can set it to any value, but we must eventually set it to T's value).

    # However, note: we are allowed to change any character (even one that is already fixed) but that would be non-optimal. So we only change the differing characters.

    # But the problem: we must produce the lexicographically smallest sequence of states.

    # How to approach:

    # We have m differing positions. We must fix each one exactly once. The operations are independent in the sense that we can fix one at a time.

    # However, we can also change a character that is not yet fixed to a value that is not T's value? But then we have to fix it again, which would be two operations. That is not minimal. So we must fix each differing character to T's value in one operation.

    # Therefore, the sequence of states is:

    #   Operation 1: change one of the differing characters (say at index i) from S[i] to T[i] (or to something else? but then we have to fix it again, which is not minimal). So we must change it to T[i] in the first operation for that character.

    # But wait: what if we change a character to a value that is not T[i]? Then we have to change it again. That would be two operations for that character. But we are allowed to change any character, so we can change a character that is already fixed? 

    # However, the problem requires the minimum number of operations. So we cannot change a character twice. Therefore, we must fix each differing character exactly once, and we must fix them in some order.

    # But note: we are allowed to change any character, even one that is not differing? But that would be non-optimal because we are increasing the number of operations. So we only change the differing characters.

    # However, consider: what if we change a character that is not differing to a value that is not T's value? Then we have to fix it again, which is two operations. So we avoid that.

    # Therefore, the minimal sequence has exactly m operations, and in each operation we fix one differing character (changing it from S[i] to T[i]).

    # But wait: what if we fix two characters in one operation? No, because we are only allowed to change one character per operation.

    # So the minimal number of operations is m.

    # Now,