from collections import Counter

def main():
    data = list(map(int, input().split()))
    count = Counter(data)
    # We are going to consider the four-card set and the possibility of adding one card.

    # Let's extract the counts and the distinct numbers.
    # We are only concerned with the counts of the numbers that appear.

    # We'll consider the frequency counts of the four-card set.

    # Case 1: There is a number with count 3 and another with count 1.
    if max(count.values()) == 3 and len(count) == 2:
        # Then we have two distinct numbers: one with 3, one with 1.
        # We can add the one with count 1 to make it 2, so full house.
        print("Yes")
        return

    # Case 2: There is a number with count 2 and another with count 2 (so two distinct numbers, each twice).
    if max(count.values()) == 2 and len(count) == 2:
        # Then we can add one of the two numbers to get 3 and 2.
        print("Yes")
        return

    # Case 3: There is a number with count 4 (all same). Then we cannot form full house.
    if max(count.values()) == 4:
        print("No")
        return

    # Case 4: There are three distinct numbers (so the counts must be [2,1,1] or [1,1,2] etc.).
    if len(count) == 3:
        print("No")
        return

    # Case 5: There are four distinct numbers (each once).
    if len(count) == 4:
        print("No")
        return

    # But wait, what if the four-card set has two distinct numbers but counts are (4,0) is already handled by max(count.values())==4.

    # However, note: the above cases cover:
    #   Case 1: two distinct numbers, counts (3,1)
    #   Case 2: two distinct numbers, counts (2,2)
    #   Case 3: one distinct number (counts (4))
    #   Case 4: three distinct numbers (counts (2,1,1))
    #   Case 5: four distinct numbers (counts (1,1,1,1))

    # But what if the four-card set has two distinct numbers but counts (3,1) or (2,2) we already handled.

    # However, note: the four-card set might have two distinct numbers but counts (1,3) which is same as (3,1) and (2,2) is same as (2,2). So we covered.

    # But wait, what if the four-card set has two distinct numbers but counts (4,0) is one distinct number.

    # Actually, the above cases are exhaustive for four-card sets.

    # However, there is one more possibility: the four-card set might have two distinct numbers but counts (3,1) or (2,2) and we handled.

    # But note: the four-card set might have two distinct numbers with counts (3,1) or (2,2) and we handled.

    # But wait, what if the four-card set has two distinct numbers with counts (1,3) (same as (3,1)) and (2,2). We handled.

    # But there is a possibility that the four-card set has two distinct numbers but the counts are (4,0) (one distinct) and (3,1) and (2,2) are the only two ways to split four into two distinct numbers.

    # Therefore, we have covered all cases.

    # However, note: the above code returns in the cases we found. But what if none of the cases match? Then we print "No".

    # But wait, we have an if for each case and then a final return? Actually, we have:

    #   Case 1: if condition -> print Yes and return.
    #   Case 2: if condition -> print Yes and return.
    #   Case 3: if condition -> print No and return.
    #   Case 4: if condition -> print No and return.
    #   Case 5: if condition -> print No and return.

    # But note: the four-card set must fall into one of these categories.

    # However, there is a possibility that the four-card set has two distinct numbers but counts (3,1) or (2,2) and we already handled.

    # But wait, what if the four-card set has two distinct numbers but counts (3,1) and we are in Case 1, then we return.

    # But note: the four-card set might have two distinct numbers