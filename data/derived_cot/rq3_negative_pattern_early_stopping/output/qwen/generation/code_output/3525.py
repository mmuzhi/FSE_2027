class Solution:
    def maxEnergyBoost(self, energyDrinkA: List[int], energyDrinkB: List[int]) -> int:
        n = len(energyDrinkA)
        # If only one hour, return the max of the two
        if n == 1:
            return max(energyDrinkA[0], energyDrinkB[0])
        
        # Initialize the dp states for the first hour
        dp0 = energyDrinkA[0]  # ending with A
        dp1 = energyDrinkB[0]  # ending with B
        
        # Iterate from the second hour (index 1) to the last
        for i in range(1, n):
            new_dp0 = max(dp0 + energyDrinkA[i], dp1)  # Switching from B to A gives 0 for this hour, so only dp1 (previous state) plus 0
            new_dp1 = max(dp1 + energyDrinkB[i], dp0)  # Switching from A to B gives 0 for this hour, so only dp0 (previous state) plus 0
            dp0, dp1 = new_dp0, new_dp1
        
        return max(dp0, dp1)