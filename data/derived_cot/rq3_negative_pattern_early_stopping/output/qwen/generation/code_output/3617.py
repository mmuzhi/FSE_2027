class Solution:
    def possibleStringCount(self, word: str) -> int:
        # Break the word into runs
        runs = []
        if not word:
            return 0
        count = 1
        for i in range(1, len(word)):
            if word[i] == word[i-1]:
                count += 1
            else:
                runs.append(count)
                count = 1
        runs.append(count)
        
        # For each run, the number of choices is (run_length) if we consider that the intended run length can be from 1 to run_length (but then the output run length is intended + (0 or 1) and must be exactly the given run_length.
        # But note: the intended run length must be at least 1 and at most run_length, and the output run length is intended + (0 or 1) = run_length.
        # So intended run length can be run_length or run_length - 1 (if run_length >= 2) or only run_length if run_length == 1.
        # But wait, the above is not the only possibility. Actually, the intended run length can be any value from 1 to run_length, but then the output run length must be intended + (0 or 1) and must equal run_length.
        # So intended + (0 or 1) = run_length -> intended = run_length or run_length - 1 (if run_length >= 2).
        # But also, intended must be at least 1.
        # However, there is another way: the intended run length can be any value from 1 to run_length, but then the output run length is intended + (0 or 1) and must be exactly run_length.
        # So intended can be run_length - k, where k is 0 or 1, but also, if intended is run_length - k, then run_length - k + (0 or 1) = run_length -> k can be 0 or 1, but also, intended must be positive.
        # Actually, the condition is: intended + (0 or 1) = run_length.
        # So intended = run_length - 0 or run_length - 1.
        # But also, intended must be at least 1.
        # So for a run of length L, the intended run length can be L or L-1 (if L>=2) or only L if L==1.
        # But then, the number of choices for a run is:
        #   if L == 1: 1
        #   if L >= 2: 2
        # However, the example "aaaa" (L=4) would then have 2 choices, but the expected output is 4.

        # Let me re-think with "aaaa":
        # The intended string must be a string of 'a's. The output is "aaaa".
        # The intended string can be:
        #   "aaaa": then output can be "aaaa" (0 extra) or "aaaaa" (1 extra) -> but output is "aaaa", so valid if 0 extra.
        #   "aaa": then output can be "aaaa" (1 extra) or "aaaaa" (2 extra) -> but output is "aaaa", so valid if 1 extra.
        #   "aa": then output can be "aaa" (1 extra) or "aaaa" (2 extra) -> valid if 2 extra? But the problem says "at most once", meaning per run, you can add at most one extra. So for "aa", the output can be "aa" or "aaa", not "aaaa". -> invalid.
        #   "a": then output can be "a" or "aa", not "aaaa". -> invalid.
        # So only 2.

        # But the example output is 4.

        # This indicates that the problem might be interpreted differently.

        # Alternative interpretation:
        # The operation is: Alice might have pressed a key for too long, resulting in a character being typed multiple times, but she did this at most once. This means that in the intended string, each character is typed once, but in the output, each character might be repeated 0 or 1 times consecutively. 

        # But then, the intended string is not necessarily the same as the output's run boundaries. 

        # Actually, the problem is: 
        # We are given the output string. We need to find the number of strings S such that S can be obtained from the output by removing at most one extra repetition for each run. 

        # But note: the problem says "at most once", meaning for each run in the output, we can remove at most one repetition (if any) to get the intended string.

        # So for a run of length L in the output,