import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    p_list = list(map(int, data[1:1+n]))
    
    # We'll create an array "ans" of length n (the final array) and mark which numbers are present.
    # But we need to determine the order.

    # Alternatively, we can use a Fenwick tree to count the number of insertions that occurred before a certain position and then determine the final position.

    # However, there is a simpler idea: 
    # We can simulate the insertions by keeping track of the current length and the positions of the numbers, but that is O(n^2).

    # Another idea: 
    # We can use a balanced tree or a sorted list to keep the positions of the numbers, but we need to update the positions for all numbers after an insertion.

    # Insight: 
    # The final array is the same as if we start with an empty array and for each i from 1 to N, we insert i at position P_i, and then the array is built.

    # We can use a data structure that supports fast insertion and deletion at arbitrary positions, but we are only inserting and the array grows.

    # We can use a linked list with an array of next pointers and a pointer to the head, but then we need to update the head and the next pointers for each insertion. However, we need to output the entire array at the end.

    # But note: we are only inserting, and the array is built from left to right. We can use a list and insert at the desired position, but that is O(n) per insertion and O(n^2) total.

    # We need a better way.

    # Let's try to compute the final position of each number without simulation.

    # Consider: 
    #   Let f(i) be the final position of the number i.
    #   Initially, the number i is inserted at position P_i, but then every subsequent insertion that occurs at a position <= f(i) (or <= the position where i was inserted) will shift i to the right.

    # Actually, the shift happens for insertions that occur after i and that insert at a position <= the current position of i (at the time of insertion) or <= the position where i was inserted? 

    # Actually, when we insert a number j (j>i) at position P_j, then if P_j <= the current position of i (at the time of j's insertion) then i is shifted right by one. But note: the current position of i at the time of j's insertion is not the final position.

    # Alternatively, we can think: 
    #   The final position of i is: 
    #       initial_position = P_i - 1 (0-indexed) 
    #       Then, for each j from i+1 to N, if P_j <= (initial_position + 1 + number of shifts that have occurred at the time of j's insertion) then the position of i increases by 1.

    # But the shifts that have occurred at the time of j's insertion are the insertions k (from i+1 to j-1) that inserted at a position <= (the position of i at the time of k's insertion + 1) ??? 

    # This seems complicated.

    # Another idea: 
    #   We can use a stack or a queue? 

    # Let's try to reverse the process:

    #   We start with an array of size N (with numbers 1 to N) and then we remove the insertions in reverse order.

    #   Operation N: inserted at position P_N. Then the array before the last insertion was: 
    #        [A_0, A_1, ..., A_{N-1}] = [A_0, A_1, ... , A_{P_N-2}, N, A_{P_N-1}, ... , A_{N-1}]
    #   So to remove the last insertion, we take the last element and put it at the position P_N-1 (0-indexed) and then the array becomes the array without N.

    #   But note: the array without N is the array after N-1 operations.

    #   However, the positions in the previous operations are defined with respect to the array at that time, and the array length was N-1.

    #   We can do:

    #       Let A be the final array (size N).
    #       Let B be the array after N-1 operations (size N-1).
    #       Then, A is obtained by inserting N at position P_N in B.

    #   So to reverse, we remove N from A at position P_N-1 (0-indexed) and then the array becomes B.

    #   But then