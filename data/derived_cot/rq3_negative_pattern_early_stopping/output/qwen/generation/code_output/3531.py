class Solution:
    def minDamage(self, power: int, damage: List[int], health: List[int]) -> int:
        # Combine the damage and health into a list of tuples
        enemies = sorted(zip(damage, health), key=lambda x: x[1] / x[0], reverse=True)
        total_time = 0
        total_damage = 0
        for d, h in enemies:
            time_needed = (h + power - 1) // power
            total_time += time_needed
            # The damage from this enemy is d * total_time (because it was alive for total_time seconds)
            total_damage += d * total_time
        return total_damage