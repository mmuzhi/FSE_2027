from typing import List
import collections
import bisect

class TopVotedCandidate:
    def __init__(self, persons: List[int], times: List[int]):
        self.times = times[:]
        self.persons = []
        votes = collections.defaultdict(int)
        max_votes = 0
        leader = 0

        for i in range(len(times)):
            p = persons[i]
            votes[p] += 1
            if votes[p] >= max_votes:
                leader = p
                max_votes = votes[p]
            self.persons.append(leader)

    def q(self, t: int) -> int:
        idx = bisect.bisect_right(self.times, t) - 1
        return self.persons[idx]