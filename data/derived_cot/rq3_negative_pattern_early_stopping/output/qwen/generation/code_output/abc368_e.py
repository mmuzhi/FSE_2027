import sys
from collections import defaultdict, deque

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    
    it = iter(data)
    n = int(next(it)); m = int(next(it)); x1 = int(next(it))
    
    # We are given m trains. Each train: A, B, S, T.
    trains = []
    for i in range(m):
        a = int(next(it)); b = int(next(it)); s = int(next(it)); t = int(next(it))
        trains.append((a, b, s, t))
    
    # We are to assign X_2, ..., X_M. Note: the first train is train0 (index0) and has X_0 = x1 (given).
    # We'll compute Y_j = X_j + S_j for each train j.
    # For train0: Y0 = x1 + trains[0][2]
    
    # We need to consider constraints: for each train j (index j) and for each train i (index i) such that:
    #   B_i = A_j and T_i <= S_j (the original S_j) then Y_j >= T_i + Y_i - S_i.
    #
    # We can reorganize by city and by time.
    #
    # Let's create:
    #   For each city, we want to collect the trains that depart from that city (for the condition of being the start of a transfer) and the trains that arrive at that city (for the condition of being the end of a transfer).
    #
    # But note: the condition for a train j (which departs from A_j) is determined by the trains i that arrive at A_j (i.e., B_i = A_j) and have T_i <= S_j (the original S_j).
    #
    # We can precompute for each city c, the list of (train_index, T_i, S_i) for trains that end at c (i.e., B_i = c) and also the list of (train_index, S_j, T_j) for trains that depart from c (i.e., A_j = c) but note the condition for a train j (departing from c) is determined by the trains i that end at c and have T_i <= S_j (the original S_j of train j).
    #
    # However, note: the condition for train j (which departs from c) is determined by the trains i that end at c and have T_i <= S_j (the original S_j of train j). 
    #
    # We can do:
    #   For each city c, we want to know: for a given train j (departing from c) with original departure time S_j, what is the maximum (T_i + Y_i - S_i) for all trains i that end at c and have T_i <= S_j.
    #
    # Then Y_j must be at least that maximum.
    #
    # We can precompute for each city c:
    #   Let events = list of (T_i, S_i, train_index) for all trains i that end at c (i.e., B_i = c).
    #   Then, for a train j (departing from c) with original departure time S_j, we want the maximum (T_i + Y_i - S_i) for all events (T_i, S_i) with T_i <= S_j.
    #
    # But note: the value (T_i + Y_i - S_i) for a train i depends on Y_i, which is the solution for train i. So we need to compute Y_i first.
    #
    # We can process the trains in increasing order of S_j (the original departure time). Why?
    #   Because the constraint for a train j (departing from city c) depends on trains i that end at c and have T_i <= S_j (the original S_j). 
    #   If we process in increasing order of S_j, then when we process train j, all trains i that end at c and have T_i <= S_j (original) have been processed (if we process by increasing S_j, then the trains i that end at c and have T_i <= S_j are the ones we've already processed? Not exactly: note that the condition for train j is about the original S_j, and the trains i that end at c and have T_i <= S_j (original) might have been processed (if their S_i is not directly related) but note: the constraint for train j is independent of the departure time of train i (S_i) but only uses T_i and S_i (which are fixed) and Y_i (which we compute). 
    #
    # However, note: the condition for train j (departing from c) is determined