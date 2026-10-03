import sys
from functools import lru_cache

sys.setrecursionlimit(10000)

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    
    n = int(data[0]); m = int(data[1]); l = int(data[2])
    A = list(map(int, data[3:3+n]))
    B = list(map(int, data[3+n:3+n+m]))
    C = list(map(int, data[3+n+m:3+n+m+l]))
    
    total_cards = n + m + l
    # Combine the three lists into one list of numbers
    cards = A + B + C
    # The initial state: first n cards are Takahashi (0), next m Aoki (1), last l table (2)
    # We'll represent the state as a tuple of length total_cards, each element is 0,1, or 2.
    # But we need to know the numbers for each card. We have the list "cards" which is the entire set.
    # We'll use memoization with state and turn (0 for Takahashi, 1 for Aoki)
    
    # But wait, the initial state is fixed: the first n cards are 0, next m are 1, last l are 2.
    # However, the state is defined by the assignment of each card to 0,1,2. But the initial state is:
    # state0 = (0,)*n + (1,)*m + (2,)*l
    # But the game starts with Takahashi's turn (turn=0).
    
    # We'll use a recursive function with memoization. The state is (state_tuple, turn) but we can encode turn in the state_tuple? 
    # Alternatively, we can have two separate arguments: the state (tuple of length total_cards) and the turn (0 or 1).
    # But the state is the entire assignment, so we can use the state as a tuple and turn as a separate integer.
    
    # However, the state is the entire assignment, so we can use the state as a tuple and turn as a separate integer.
    # But the state is a tuple of length total_cards (each element 0,1,2) and turn is 0 or 1.
    
    # But the state space is 3^(total_cards) * 2, which is acceptable for total_cards <= 12 (max 1 million states).
    
    # But wait, we need to know the numbers for each card. We have the list "cards", so we can access the number of a card by its index.
    
    # The moves:
    # For Takahashi's turn (turn=0): he can choose any card that is in his hand (state[i] == 0) and play it (set state[i] to 2). Then, after that, he can choose to take one card from the table (state[j] == 2) that has a number less than the card he played (cards[i]) and set state[j] to 0. But note: the card he played is now on the table, so the table includes the card i. Then, he can take any one card from the table (any j with state[j]==2) that satisfies cards[j] < cards[i]. But wait, the card i is now on the table, so it's included in the table. But the condition is: after playing, if there is a card on the table (including the one just played) with a number less than the played card, then he can take one such card. But note: the card he just played is now on the table, so it is included. But the condition is "less than", so if the card he played is x, then he can take any card on the table (including the one he just played) that is less than x? But wait, the problem says: "if there is a card on the table with a number less than the number on the card he just played, he may take one such card". So, the card he just played is now on the table, but its number is x, and if there is a card with number < x, then he can take one. But note: the card he just played is x, so if there is a card with number < x, then he can take it. But the card he just played is x, so it doesn't count as less than x. So, the condition is on the table (which now includes the card i) but the card i (x) is not less than x. So, the condition is: there exists a card j (j != i) on the table (state[j]==2) such that cards[j] < cards[i]? Actually, no: the problem says "if