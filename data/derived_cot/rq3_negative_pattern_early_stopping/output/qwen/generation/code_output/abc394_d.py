def main():
    S = input().strip()
    stack = []
    # Define a mapping for matching brackets
    matching = {')': '(', ']': '[', '>': '<'}
    # We'll traverse each character in the string
    for char in S:
        if char in '([{<':
            stack.append(char)
        else:
            # If the stack is empty, then there's no opening bracket to match, so invalid.
            if not stack:
                print('No')
                return
            top = stack.pop()
            # Check if the top is the matching opening bracket for the current closing bracket
            if top != matching[char]:
                print('No')
                return
    # After processing, if the stack is not empty, there are unmatched opening brackets.
    if stack:
        print('No')
        return
    print('Yes')

if __name__ == '__main__':
    main()