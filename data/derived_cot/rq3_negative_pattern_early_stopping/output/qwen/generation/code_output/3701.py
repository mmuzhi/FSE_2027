class Solution:
    def minCostGoodCaption(self, caption: str) -> str:
        n = len(caption)
        # We'll consider that the entire string must be partitioned into runs of at least 3.
        # But note: the problem does not require that the entire string is one run. It can be multiple runs, each of length >=3.
        # However, the minimal operations might be achieved by converting the entire string to one letter (if that's possible with fewer operations) or by having multiple runs.

        # But note: the problem says "every character appears in groups of at least 3 consecutive occurrences". This means that the string is a concatenation of runs, each run being a single character repeated at least 3 times.

        # We are allowed to change each character independently. We can think of the problem as: we want to assign a target letter to each position, such that the target letters form a sequence of runs (each run is a single letter repeated) and each run has length at least 3. The cost is the sum of absolute differences (in terms of letter positions) between the original and target letters. We want to minimize the total cost, and if multiple, choose lexicographically smallest.

        # However, the state space is too large to try all possibilities. We need a dynamic programming approach.

        # Let's define:
        # dp[i][j] = minimal cost for the prefix ending at position i, with the last run being of letter j (where j is from 0 to 25) and the run length is at least 3 (if the run is still ongoing) or we can consider the run length.

        # But note: the entire string must be partitioned into runs. The runs are contiguous and each run is a single letter.

        # Alternatively, we can consider that the entire string must be partitioned into segments (runs) of length at least 3. The transitions would be: at position i, we can either start a new run (if the previous run ended at least 3 characters ago) or continue the current run.

        # But the state must remember the last run's letter and the length of the current run.

        # However, the string length is up to 50,000. We need an efficient DP.

        # Let's define:
        # dp[i][c] = minimal cost for the prefix up to index i, with the current run being letter c (from 0 to 25) and the current run length is (i - start + 1). But we need to know the start of the current run.

        # Alternatively, we can use a DP that considers the last two or three characters to enforce the run length condition.

        # Actually, we can use a DP that goes by positions and for each position, we consider the last run's letter and the length of the current run. But the state space would be 26 * (length) which is 26 * 50000, which is 1.3e6, which is acceptable in Python if implemented carefully.

        # But we also need to consider that the run must be at least 3. So when we are at position i, if we are in a run of letter c, then the run length is (i - start + 1). We must have at least 3 in the current run to close it? Actually, we can close the run at any time, but we must have at least 3 in the run.

        # Actually, the problem does not require that the runs are separated by different letters. But by definition, a run is a maximal sequence of the same letter. So if we have "aaaabbbb", then the runs are "aaaa" and "bbbb". But if we have "aaaabbaaaa", then the runs are "aaaa", "bbb", and "aaaa". But wait, the condition is that every character appears in groups of at least 3. So the entire string must be partitioned into runs of at least 3. Therefore, we cannot have a run of length 2 or 1.

        # So the entire string must be partitioned into runs of at least 3. This means that the string length must be at least 3, and the runs must be contiguous and non-overlapping.

        # Now, the problem is: we can change each character arbitrarily (with cost being the absolute difference in letter positions) to form a string that is a concatenation of runs of at least 3. We want the minimal total cost, and lexicographically smallest if multiple.

        # We can use DP with state (i, last_letter, run_length) where:
        #   i: current index (0-indexed)
        #   last_letter: the letter (0-25) that the current run is in (if any)
        #   run_length: the length of the current