class Solution:
    def minTime(self, skill: List[int], mana: List[int]) -> int:
        n = len(skill)
        m = len(mana)
        # We'll create a 2D array to store the finish times for each wizard and potion.
        # But note: n and m can be up to 5000, so a 2D array of size 5000x5000 is 25e6 elements, which is acceptable in C++ but in Python might be heavy.
        # Alternatively, we can use dynamic programming with two arrays (current and previous) to save memory.
        # But let's first try with a 2D array.

        # However, we can optimize by noticing that the start time for potion j at wizard i is the maximum of:
        #   finish time of potion j at wizard i-1 (if i>0)
        #   finish time of potion j-1 at wizard i (if j>0)
        # But actually, the finish time for potion j at wizard i is start_time + skill[i]*mana[j], and start_time is the maximum of the two.

        # We can use a DP table: dp[i][j] = finish time at wizard i for potion j.

        # But we can also use two 1D arrays: one for the current wizard's finish times for all potions, and one for the previous wizard.

        # Alternatively, we can use a greedy approach: sort the wizards by their skills? Or sort the potions by mana? 

        # But note: the processing time for a potion j on wizard i is skill[i] * mana[j]. 

        # We can use the following idea: 
        #   Let F(i, j) = finish time at wizard i for potion j.
        #   Then F(i, j) = max(F(i, j-1), F(i-1, j)) + skill[i] * mana[j]

        # But wait, is that correct? 

        # Actually, the start time for potion j at wizard i is the maximum of:
        #   F(i, j-1) (the time wizard i finishes the previous potion)
        #   F(i-1, j) (the time the previous wizard finishes potion j)

        # Then F(i, j) = start_time + skill[i] * mana[j]

        # So we can write:
        #   F(0,0) = skill[0] * mana[0]
        #   For i=0, j>=1: F(0, j) = max(F(0, j-1), 0) + skill[0]*mana[j]   [but actually, the previous wizard for j is not defined for i=0, so we only consider F(0, j-1)]
        #   For j=0, i>=1: F(i, 0) = max(F(i-1, 0), F(i, -1)) + skill[i]*mana[0]   [but F(i, -1) is not defined, so we only consider F(i-1,0)]
        #   For i>=1 and j>=1: F(i, j) = max(F(i, j-1), F(i-1, j)) + skill[i]*mana[j]

        # But wait, the example: 
        #   skill = [1,5,2,4], mana = [5,1,4,2]
        #   F(0,0) = 1*5 = 5
        #   F(1,0) = max(F(0,0), F(1,-1)) + 5*5 -> but F(1,-1) is not defined. Actually, for j=0 and i=1, the start time is F(0,0)=5, so F(1,0)=5+25=30.
        #   F(0,1) = max(F(0,0), F(-1,1)) + 1*1. But F(-1,1) is 0? Then start time is max(5,0)=5, so F(0,1)=5+1=6. But the example starts at 52 for wizard0 on potion1.

        # That doesn't match. 

        # Let me reexamine the example: 
        #   The example says that if wizard0 starts potion1 at time 50, then at time 58, wizard2 is done with potion1, but wizard3 is still working on potion0 (until 60). 

        # The constraint is that the same potion must be processed in order, but also the same wizard cannot process two potions at once. 

        # Actually, the start time for potion j at wizard i is the maximum of