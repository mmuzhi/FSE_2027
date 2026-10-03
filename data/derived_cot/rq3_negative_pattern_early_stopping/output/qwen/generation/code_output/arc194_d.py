import sys
from collections import deque

MOD = 998244353

def main():
    data = sys.stdin.read().splitlines()
    n = int(data[0])
    s = data[1].strip()
    
    # We are going to use a DP approach. 
    # Observation: The operations allow reversing any contiguous valid substring. 
    # This is similar to being able to rearrange the parentheses arbitrarily, but with the constraint that we can only reverse valid substrings.

    # However, note that the problem is about distinct strings. 

    # After reading some known problems, I recall that the answer is often 1 or 2. 
    # In fact, the sample answers are 2 and 1.

    # Another observation: 
    # Operation 1: Reverse the entire string. This is allowed because the entire string is valid. 
    # Operation 2: Reverse any valid substring. 

    # But note: reversing a substring that is a palindrome doesn't change it. 

    # However, the key is that the operations allow us to "move" parentheses around, but only in a way that preserves the validity of the substring being reversed.

    # Actually, there is a known problem: "Minimum flips to make the parenthesis balanced" but not exactly.

    # Alternatively, consider that the set of reachable strings might be the set of all strings that have the same "nesting structure" as the original.

    # But wait, the problem is about reversing valid substrings. 

    # There is a known result: 
    # In fact, the problem is equivalent to being able to rearrange the parentheses arbitrarily as long as the total number of '(' and ')' remains the same and the string remains a valid parenthesis sequence? 

    # But wait, the operation allows reversing a valid substring, which might change the order. 

    # However, note that reversing a valid substring is not necessarily a rearrangement that preserves the nesting. 

    # But wait, there is a known problem: "String Transformation" where you can reverse any substring that is a palindrome. But here, the substring must be valid, not necessarily a palindrome.

    # After some thought, I recall that the answer is often 1 or 2. 

    # In fact, the answer is 1 if the string is a palindrome (after reversal, it's the same) and 2 otherwise. 

    # But wait, in the sample: 
    # "()" is a palindrome and the answer is 1.
    # "(()())" is not a palindrome, but the answer is 2.

    # But wait, "(()())" reversed is "()(())", which is different. 

    # However, can I get more than 2? 

    # Let me try with "(()())": 
    # Operation 1: Reverse entire string -> "()(())"
    # Operation 2: Reverse the entire string again -> "(()())" — back to start.
    # Operation 3: Reverse a substring. For example, in "(()())", can I reverse a substring to get something else? 
    # Let me try reversing the substring from index 0 to 1: "((" — not valid.
    # Index 0 to 2: "(()" — not valid.
    # Index 0 to 3: "(()(" — not valid.
    # Index 0 to 4: "(()()" — valid? 
    # Let me check: "(()()" — 
    # '(' -> push
    # '(' -> push
    # ')' -> pop (now stack has one '(')
    # '(' -> push (now stack has one '(' and then one more)
    # ')' -> pop (now stack has one '(') — not empty. So not valid.
    # Index 1 to 4: "()((" — not valid.
    # Index 2 to 5: "())" — not valid.
    # So only the entire string can be reversed.

    # So from "(()())", I can only get two distinct strings: the original and the reversed.

    # Similarly, for "((()))", I can only get two distinct strings: the original and the reversed.

    # But wait, what about a string like "()(())" (which is the reversed of "(()())")? 
    # Now, reversing the entire string of "()(())" gives "(()())", so again two.

    # What about a string like "()()": 
    # Original: "()()"
    # Reversed: "()()" — same. 
    # But wait, reversing the entire string: 
    # Original: "()()"
    # Reversed: "()()" — same. 
    # But can I reverse a substring? 
    # For example, the substring "()()" is valid, but reversing it gives "()()" — same.
    # Or the substring "()" (at