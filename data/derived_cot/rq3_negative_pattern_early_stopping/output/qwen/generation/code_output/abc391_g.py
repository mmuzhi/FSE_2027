def main():
    import sys
    data = sys.stdin.read().splitlines()
    if not data: 
        return
    parts = data[0].split()
    n = int(parts[0])
    m = int(parts[1])
    S = data[1].strip()
    
    # Precompute transition table for states 0 to n (state n is absorbing)
    # For each state i (0 <= i <= n) and each character c (0-25), compute next state j.
    # We'll map characters to 0-25, but S is given in lowercase, so we can use ord(c) - ord('a')
    # But we can precompute for each state i and each letter (0-25) the next state.
    # The next state from i with letter c is the smallest j >= i such that S[j] == c, if exists, else i (but actually, we can stay at i? But note: we are matching the subsequence, so if we are at state i and we see a character c, we can only extend if the next character in S (starting from i) is c. But actually, we can skip characters arbitrarily, so the next state is the smallest j >= i such that S[j] == c, and if no such j, then we stay at i? Actually, no: the state i means we have matched the first i characters. Then, we look for the next occurrence of c in S from position i onward. But note: we are allowed to use the same character multiple times? No, because S is fixed and we are matching a subsequence. But the same character in S can be used only once. So, we are effectively building a subsequence of S.

    # Actually, the standard automaton for matching a subsequence is: 
    #   state i: we have matched the first i characters of S.
    #   On character c, we look for the next occurrence of c in S starting from index i. Let j be the smallest index >= i such that S[j] == c. Then, if j < n, we can set the next state to j+1? No, because we are matching the subsequence, and we are allowed to skip characters arbitrarily. Actually, the next state should be the next state after matching c. But note: we are matching the entire subsequence. The automaton for matching a subsequence is: from state i, if we see c and S[i] == c, then we go to state i+1. But if S[i] != c, we stay at i. But that is not correct because we can skip characters. 

    # Actually, the correct automaton for matching the longest prefix of S as a subsequence is:
    #   state i: we have matched the first i characters of S.
    #   On character c, we set j = i, and then while j < n and S[j] != c: j++.
    #   Then, if j < n and S[j] == c, then we set i = j+1 (because we matched one more character). But wait, that would be matching the entire string S? No, because we are matching the subsequence. Actually, the automaton should be: from state i, we look for the next occurrence of c in S starting from i. Then, the next state is the index after that occurrence? Actually, no: the state should be the length of the matched prefix. So, if we are at state i and we see c, then we set the next state to the smallest j >= i such that S[j] == c, and then the state becomes j+1? But that would be incorrect because we are matching the entire string S, but we are allowed to have non-contiguous matching. Actually, the state should be the length of the matched prefix. So, if we are at state i, and we see c, then we set the next state to the smallest j >= i such that S[j] == c, and then the state becomes j+1? No, because the state is the length of the matched prefix. Actually, the state i means we have matched the first i characters. Then, when we see c, we can only extend the subsequence if the next character in S (at position i) is c. But that is not correct because we can skip characters. 

    # Let me clarify with an example: S = "abc", and T = "acb". 
    #   Start at state 0.
    #   First character 'a': matches S[0], so state becomes 1.
    #   Second character 'c': now, from state 1, we look for 'c' in S starting from index 1. We find S[2]=='c'. Then, we