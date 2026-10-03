class Solution:
    def satisfiesTrip(self, mid, time, totalTrip):
        trip = 0
        for t in time:
            trip += mid // t
        return trip >= totalTrip

    def minimumTime(self, time: list, totalTrips: int) -> int:
        time.sort(reverse=True)
        minimum = min(time)
        left = minimum
        right = minimum * totalTrips
        while left < right:
            mid = (left + right) // 2
            if self.satisfiesTrip(mid, time, totalTrips):
                right = mid
            else:
                left = mid + 1
        return left