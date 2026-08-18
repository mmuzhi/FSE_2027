import random


class BlackjackGame:
    def __init__(self):
        self.deck = self.createDeck()
        self.playerHand = []
        self.dealerHand = []

    def createDeck(self):
        deck = []
        suits = ["S", "C", "D", "H"]
        ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        for suit in suits:
            for rank in ranks:
                deck.append(rank + suit)
        random.Random().shuffle(deck)
        return deck

    def calculateHandValue(self, hand):
        value = 0
        numAces = 0
        for card in hand:
            rank = card[:-1]
            if rank.isdigit():
                value += int(rank)
            elif rank in ("J", "Q", "K"):
                value += 10
            elif rank == "A":
                value += 11
                numAces += 1
        while value > 21 and numAces > 0:
            value -= 10
            numAces -= 1
        return value

    def checkWinner(self, playerHand, dealerHand):
        playerValue = self.calculateHandValue(playerHand)
        dealerValue = self.calculateHandValue(dealerHand)
        if playerValue > 21 and dealerValue > 21:
            return "Player wins" if playerValue <= dealerValue else "Dealer wins"
        elif playerValue > 21:
            return "Dealer wins"
        elif dealerValue > 21:
            return "Player wins"
        else:
            return "Player wins" if playerValue > dealerValue else "Dealer wins"


if __name__ == "__main__":
    game = BlackjackGame()
    # Match Java List.toString() output format: [elem, elem, ...]
    print("[" + ", ".join(game.deck) + "]")
    print(game.calculateHandValue(["QD", "9D", "JC", "QH", "AS"]))
    print(game.checkWinner(["QD", "9D", "JC", "QH", "AS"],
                           ["QD", "9D", "JC", "QH", "2S"]))