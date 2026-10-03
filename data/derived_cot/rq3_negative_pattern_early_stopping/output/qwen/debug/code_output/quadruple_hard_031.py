class Solution:
    def longestValidSubstring(self, word: str, forbidden: List[str]) -> int:
        if not word:
            return 0
        
        trie = {}
        for f in forbidden:
            t = trie
            for c in f:
                if c not in t:
                    t[c] = {}
                t = t[c]
            t['end'] = True
            t['length'] = len(f)
        
        state = trie
        j = 0
        res = 0
        
        for i in range(len(word)):
            state = trie
            while j < len(word):
                c = word[j]
                if c in state:
                    state = state[c]
                    if 'end' in state:
                        forbidden_length = state['length']
                        j = j - forbidden_length + 1
                        break
                    if 'length' in state and j - state['length'] + 1 >= i:
                        j = j - state['length'] + 1
                        break
                else:
                    break
                j += 1
            res = max(res, j - i)
        return res