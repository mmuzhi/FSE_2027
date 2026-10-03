class Solution:
    def maxFreeTime(self, eventTime: int, k: int, startTime: List[int], endTime: List[int]) -> int:
        # Calculate the total meeting time (sum of durations)
        total_meeting_time = 0
        for i in range(len(startTime)):
            total_meeting_time += (endTime[i] - startTime[i])
        return eventTime - total_meeting_time