def main():
    s = input().strip()
    n = len(s)
    # We'll use a list to represent the string for efficient replacement
    arr = list(s)
    i = 0
    # We'll use a while loop that breaks when we don't find a WA in a full pass
    # But we can do a single pass that replaces all WA's? Actually, the problem requires leftmost first, and then the next leftmost, etc.

    # However, note: the replacement of one WA might create a new WA that is to the left of the current position? 
    # But the operation is defined to replace the leftmost WA. So we must replace the first WA we find, then restart from the beginning? 

    # But the problem says: "as long as the string contains WA", so we can do:

    # We'll use a while loop that breaks when no WA is found in a complete pass.

    # But we can do a more efficient method: 
    #   We traverse the string and whenever we find "WA", we replace it with "AC", and then we set the current index to the next character after the replacement, but then we must check from the beginning again because the replacement might have created a WA that starts at the beginning.

    # However, note: the replacement is two characters. The leftmost WA must be the first occurrence. So we can do:

    #   We'll traverse from left to right, and when we find "WA", we replace it and then set the current index to the position after the replacement (i+2) and then continue from there? 

    # But wait, what if the replacement creates a WA that starts at the character before the replacement? 

    # Example: 
    #   String: "WAWA"
    #   We find the first WA at index0: replace with AC -> becomes "ACWA". Then we set i to 2 (index0+2). Then we continue from index2: we see "WA" at index2? Then we replace that with AC -> "ACAC". 

    # But the leftmost WA in "WAWA" is at index0, then after replacement, the string is "ACWA", and the leftmost WA is at index2. 

    # However, consider: 
    #   String: "WWA"
    #   We find the first WA at index1 (if we start at index0, we see 'W' then 'W' at index1, then at index2 we have 'A' so WA is from index1 to index2). 
    #   We replace that with AC, so the string becomes "WAC". Then we set i to 3 (index1+2) which is beyond the string. But then we break. 

    # But wait, after replacement, the string is "WAC", and we must check from the beginning again because the first two characters form WA.

    # So we cannot simply jump two characters and then continue. We must restart the scanning from the beginning.

    # However, the problem says "leftmost", so we must always start from the beginning.

    # But the length of the string is up to 300000, and if we do a full scan for each WA, worst-case we might have O(n^2) operations.

    # We need a linear solution.

    # Alternate efficient approach:

    # We can use a stack or a state machine that goes through the string once.

    # Idea: 
    #   We traverse the string and whenever we see a 'W', we start waiting for an 'A'. Then when we see an 'A', we replace the last 'W' we saw with 'A' and then the 'A' with 'C'. But note, the replacement is two characters: WA becomes AC.

    #   However, the problem requires replacing the leftmost WA. 

    #   We can use a stack:

    #   Let's define a stack that will hold the characters. But we need to know the positions.

    #   Alternatively, we can use a two-pointer that marks the positions that are not replaced.

    #   We can do:

    #       Let i = 0
    #       We'll create a new string or modify the string in a single pass.

    #   But note: the replacement might be done multiple times and the same character might be part of multiple WA's? 

    #   Actually, the problem says: replace the leftmost WA. So the first WA is replaced, and then the string changes. 

    #   We can use a greedy approach: 

    #       We traverse the string and whenever we find "WA", we replace it with "AC", and then we set a flag that we have to restart the scanning from the beginning? 

    #   But worst-case, if we have a