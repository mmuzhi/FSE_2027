import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1+n]))
    
    # We note that the i-th alien (0-indexed) becomes adult at year i+1 (after i years, so at the (i+1)-th year)
    # We are to compute the state after N years (all aliens become adults).

    # Observation:
    # The total number of stones is conserved? Actually, no: because when an adult gives a stone, it is taken from the giver and given to the receiver. So the total stones remain the same.

    # However, note: the gifts are given at the time of each alien's adulthood. And the same stone cannot be given twice.

    # Let's denote:
    #   Let B_i be the final number of stones for the i-th alien.

    # How does the process work?
    #   For the i-th alien (0-indexed, so the i-th alien becomes adult at year i+1), at that moment:
    #       All aliens with index j <= i (0-indexed) are adults (because j <= i means they have been alive for at least j+1 years, and when j+1 <= i+1, so they have become adult by the time we reach year i+1).
    #       But note: the i-th alien is included. And the condition for giving is that the adult has at least one stone.

    #   However, the catch: the gifts given at the time of the i-th alien's adulthood are taken from the adults (including the i-th alien) that have at least one stone, and then the i-th alien receives one stone from each such adult.

    #   But note: the i-th alien is included in the set of adults and if it has at least one stone, it gives one to itself? That would be a net zero for that alien? However, the other adults (j < i) also give one to the i-th alien.

    #   Actually, the process for the i-th alien's adulthood:
    #       Let S_i be the set of adults (indices j from 0 to i) that have at least one stone at the moment just before the gift distribution.
    #       Then, the i-th alien receives |S_i| stones (one from each adult in S_i).
    #       And each adult in S_i loses one stone.

    #   But note: the adults in S_i include the i-th alien if it has at least one stone.

    #   However, the state of the adults (including the i-th alien) just before the gift distribution is the state after the previous year's events.

    #   We cannot simulate year by year for N up to 500,000.

    # Alternate approach:

    # Let's denote:
    #   Let F(i) be the number of stones the i-th alien has just before the i-th alien's adulthood (at the start of year i+1, after i years and after the previous events).

    #   Then, at the moment of the i-th alien's adulthood (year i+1):
    #       The i-th alien becomes an adult. Then, the set of adults is all j from 0 to i.
    #       The number of stones given to the i-th alien is the number of adults (from 0 to i) that have at least one stone at that moment (just before the gift distribution).
    #       But note: the adults are the ones that have become adult (so indices 0 to i) and the condition is that they have at least one stone.

    #   However, the state of the adults (including the i-th alien) just before the gift distribution is F(j) for j from 0 to i (for j < i, F(j) is the state after the previous gifts, and for j = i, F(i) is the state just before the gift distribution, which is the initial A_i plus any gifts received from previous events? Actually, no: the i-th alien hasn't received any gift from the i-th event yet, but it might have received gifts from previous events? 

    #   Actually, the i-th alien (index i) becomes adult at year i+1. Before that, it was a minor. So it didn't receive any gift until now. But the previous aliens (j < i) have given gifts to the i-th alien? No, because the gifts are given only at the time of an alien's adulthood to that alien. The i-th alien is receiving the gifts at its own adulthood from the previous adults.

    #   Actually, the i-th alien (index i) does not receive any gift from the previous aliens (j < i) until the moment of its own adulthood. But wait, the previous aliens (