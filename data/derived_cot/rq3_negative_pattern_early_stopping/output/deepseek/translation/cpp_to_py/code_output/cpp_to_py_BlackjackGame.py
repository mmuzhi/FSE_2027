import random

class BlackjackGame:
    def __init__(self):
        self.deck = self.create_deck()
        self.player_hand = []
        self.dealer_hand = []

    def create_deck(self):
        suits = ["S", "C", "D", "H"]
        ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        deck = [rank + suit for suit in suits for rank in ranks]
        rng = random.SystemRandom()
        rng.shuffle(deck)
        return deck

    def calculate_hand_value(self, hand):
        value = 0
        num_aces = 0
        for card in hand:
            rank = card[:-1]  # last character is the suit
            if "2" <= rank <= "9":
                value += int(rank)
            elif rank == "A":
                value += 11
                num_aces += 1
            else:
                if rank in ("J", "Q", "K"):
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