from typing import List

class Solution:
    def deckRevealedIncreasing(self, deck: List[int]) -> List[int]:
        def reveal(n):
            lst = list(range(n))
            ans = []
            i = 0
            while lst:
                if not (i & 1):
                    ans.append(lst.pop(0))
                else:
                    lst.append(lst.pop(0))
                i += 1
            return ans
        
        order = reveal(len(deck))
        deck.sort()
        result = [0] * len(deck)
        for card, idx in zip(deck, order):
            result[idx] = card
        return result