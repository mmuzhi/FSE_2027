import random
import os
import time

class BlackjackGame:
    def __init__(self):
        self.deck = self.create_deck()
        self.player_hand = []
        self.dealer_hand = []
    
    @staticmethod
    def create_deck():
        suits = ['S', 'C', 'D', 'H']
        ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        deck = [r + s for s in suits for r in ranks]
        try:
            seed = int.from_bytes(os.urandom(4), 'big')
            random.seed(seed)
        except:
            seed = int(time.time() * 1000000)
            random.seed(seed)
        random.shuffle(deck)
        return deck

    def calculate_hand_value(self, hand):
        value = 0
        num_aces = 0
        for card in hand:
            rank_str = card[:-1]
            if rank_str.isdigit() and '2' <= rank_str <= '9':
                value += int(rank_str)
            elif rank_str == 'A':
                value += 11
                num_aces += 1
            else:  # This includes '10', 'J', 'Q', 'K'
                if rank_str in ['J', 'Q', 'K']:
                    value += 10
                # For '10', we add 10 as well
                elif rank_str == '10':
                    value += 10
        while value > 21 and num_aces > 0:
            value -= 10
            num_aces -= 1
        return value

    def check_winner(self, player_hand, dealer_hand):
        player_value = self.calculate_hand_value(player_hand)
        dealer_value = self.calculate_hand_value(dealer_hand)
        if player_value > 21 and dealer_value > 21:
            return "Player wins" if player_value <= dealer_value else "Dealer wins"
        elif player_value > 21:
            return "Dealer wins"
        elif dealer_value > 21:
            return "Player wins"
        else:
            return "Dealer wins" if player_value <= dealer_value else "Player wins"