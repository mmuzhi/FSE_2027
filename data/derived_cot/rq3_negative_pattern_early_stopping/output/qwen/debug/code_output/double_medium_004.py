class Solution:
    def findWinners(self, matches: List[List[int]]) -> List[List[int]]:
        winners = defaultdict(int)
        losers = defaultdict(int)
        
        for match in matches:
            winners[match[0]] += 1
            losers[match[1]] += 1
        
        res_1 = []
        res_2 = []
        
        for player in winners:
            if player not in losers:
                res_1.append(player)
        
        for player, count in losers.items():
            if count == 1:
                res_2.append(player)
        
        res_1.sort()
        res_2.sort()
        
        return [res_1, res_2]