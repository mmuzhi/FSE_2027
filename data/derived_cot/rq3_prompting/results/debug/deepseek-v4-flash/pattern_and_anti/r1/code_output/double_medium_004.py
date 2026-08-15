from typing import List
from collections import defaultdict

class Solution:
    def findWinners(self, matches: List[List[int]]) -> List[List[int]]:
        winners = defaultdict(int)
        losers = defaultdict(int)

        for winner, loser in matches:
            winners[winner] += 1
            losers[loser] += 1

        no_losses = []
        one_loss = []

        for player in winners:
            if player not in losers:
                no_losses.append(player)

        for player, loss_count in losers.items():
            if loss_count == 1:
                one_loss.append(player)

        no_losses.sort()
        one_loss.sort()

        return [no_losses, one_loss]