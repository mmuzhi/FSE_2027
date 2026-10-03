def main():
    data = input().split()
    s_ab = data[0]
    s_ac = data[1]
    s_bc = data[2]

    # Check for oldest
    if s_ab == '>' and s_ac == '>':
        oldest = 'A'
    elif s_ab == '<' and s_bc == '>':
        oldest = 'B'
    elif s_ac == '<' and s_bc == '<':
        oldest = 'C'
    else:
        # According to the problem, one of these must hold, but just in case, we can try to deduce differently.
        # Actually, the above conditions are complete because the input has no contradictions.
        # But let's re-check: the conditions for oldest are mutually exclusive and cover all possibilities?
        # Actually, the above conditions are the only ways to be the oldest, so we can use the same for youngest if needed.
        # But the problem says no contradictions, so we can assume one of the above holds.
        # We'll use the same conditions for youngest if needed.
        # Since we have to output the middle, we can also determine the youngest and then the middle is the one that is not oldest and not youngest.
        # But we already determined the oldest, so we can determine the youngest similarly.

        # Let's determine the youngest separately if the oldest condition didn't hold? Actually, the above conditions are complete.

        # Alternatively, we can use the following: the middle is the one that is not the oldest and not the youngest.

        # But we don't have the youngest. Let's determine the youngest by the same method.

        # Conditions for youngest:
        if s_ab == '<' and s_ac == '<':
            youngest = 'A'
        elif s_ab == '>' and s_bc == '<':
            youngest = 'B'
        elif s_ac == '>' and s_bc == '>':
            youngest = 'C'