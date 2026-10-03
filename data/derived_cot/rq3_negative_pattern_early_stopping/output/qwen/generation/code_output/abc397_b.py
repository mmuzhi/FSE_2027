def main():
    S = input().strip()
    state = 0  # 0: expecting 'i', 1: expecting 'o'
    insertions = 0

    for c in S:
        if state == 0:
            if c == 'i':
                state = 1
            else:
                insertions += 1
                state = 1
        else:  # state == 1
            if c == 'o':
                state = 0
            else:
                insertions += 1
                state = 0

    # Now, we must ensure that the total length is even. 
    # The state machine above builds the pattern until the last character. 
    # The pattern requires that the last character is at an even position (state1). 
    # But note: the state machine does not know the total length. 

    # However, the problem does not require the pattern to be built to a fixed length. 
    # But the condition is that the string has even length and the pattern holds. 

    # The above state machine builds a string that is a supersequence of S and that matches the pattern for the positions that are built. 
    # But the pattern condition is: for every odd position, 'i'; for every even position, 'o'. 

    # The above state machine does not enforce that the entire string has even length. 

    # Actually, the state machine builds the pattern until the end of S. The total length of the built string is (original length + insertions). 

    # But note: the pattern condition is independent of the length: it requires that the k-th character (for k from 1 to the length) is 'i' if k is odd and 'o' if k is even. 

    # The above state machine ensures that the built string (the supersequence) has the pattern. 

    # However, the problem requires the string to have even length. 

    # But note: the pattern condition for even length is automatically satisfied if the built string has even length? Actually, the pattern condition is defined for the entire string. 

    # The above state machine does not require the built string to have even length. 

    # Let's check with sample input 2: "iioo"