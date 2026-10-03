from collections import Counter

def main():
    data = list(map(int, input().split()))
    count = Counter(data)
    # We need to check if there exists two distinct numbers x and y such that:
    #   count[x] >= 3 and count[y] >= 2, and x != y.
    # But note: we are allowed to use the same card only once. So we must have at least 3 of x and 2 of y, and the total distinct numbers are two.

    # However, what if there are more than two distinct numbers? We can ignore the rest.

    # Let's collect the counts of each distinct number that appears at least once.
    # We need to see if there is a pair (x, y) (x != y) such that count[x] >= 3 and count[y] >= 2.

    # But note: we are only choosing five cards. So we must have at least one number with count>=3 and another with count>=2, and the two numbers are different.

    # However, what if the same number is used for both? Then we cannot because they must be different.

    # So, we can do:
    #   Let freqs = sorted(count.values(), reverse=True)
    #   But note: we have seven cards, so the counts must add up to 7.

    # Alternatively, we can check:
    #   Let's get the distinct numbers and their counts.

    # We need to check if there exists two distinct numbers x and y (x != y) such that:
    #   count[x] >= 3 and count[y] >= 2.

    # But also, we must ensure that we don't use more than the available cards. However, the condition count[x]>=3 and count[y]>=2 already ensures that.

    # However, what if the two numbers are the same? Then we cannot use them as two different numbers. So we require two distinct numbers.

    # So, we can do:
    #   Let's create a list of the counts that are at least 2 (or more) and then check if there is a 3 or more and a 2 or more from two distinct numbers.

    # But note: we might have multiple numbers with high counts. We need to check for two distinct numbers.

    # Actually, we can do:
    #   Let's get the set of numbers that have count >= 2. Then, we need to see if there is at least one number in that set with count>=3 and the rest (at least two) from the set (but note: the two numbers must be distinct).

    # However, a simpler approach: 
    #   We need to form a full house. The full house pattern is (three of one, two of another). 

    #   We can consider: 
    #       Option 1: three of a kind (x) and two of a kind (y) with x != y.

    #   So, we can iterate over the distinct numbers and check for each pair (x, y) (x != y) if count[x] >= 3 and count[y] >= 2.

    # But note: we have only seven cards. The counts are fixed. We don't need to worry about using more than available because the condition is on the counts.

    # However, what if the same card is used in two different pairs? But we are not iterating over the cards, we are using the counts.

    # But note: the counts are the total available. So if we have, for example, three 1's and two 2's, then we can use three 1's and two 2's.

    # But what if we have three 1's and two 2's and also three 3's? Then we can form two different full houses? But we only need one.

    # So, we can simply check: 
    #   Let's get the distinct numbers and their counts.

    #   We need to check if there exists two distinct numbers x and y (x != y) such that:
    #       count[x] >= 3 and count[y] >= 2.

    # However, note: what if the two numbers are the same? Then we skip because they must be different.

    # But wait: what if we have four of a kind? For example, four 1's and two 2's. Then we can form a full house by taking three 1's and two 2's. So the condition still holds.

    # So the condition is: 
    #   There exists two distinct numbers x and y such that count[x] >= 3 and count[y] >= 2.

    # But note: we must also consider that we are only choosing five cards. The condition above ensures that we have at least three of x and two of y, so we can choose