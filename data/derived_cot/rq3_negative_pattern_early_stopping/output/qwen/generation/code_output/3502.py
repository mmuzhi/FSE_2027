class Solution:
    def numberOfSubstrings(self, s: str, k: int) -> int:
        n = len(s)
        total_substrings = n * (n + 1) // 2
        # We'll use a set to record all valid substrings (by start and end indices) to avoid duplicates.
        valid_substrings = set()
        
        # For each character, we can find all substrings that have at least k occurrences.
        # But we need to avoid counting the same substring multiple times.
        # Instead, we can iterate over each starting index and use a two-pointer to find the minimal substring that has at least k of a particular character, then extend and mark all substrings that include that minimal substring as valid for that character.
        # But that might be complex.
        
        # Alternatively, we can use a different approach: for each character, record the positions where it occurs. Then, for each occurrence, we can consider the gaps between consecutive occurrences and then determine the minimal substring that has k occurrences of that character.
        # But then, how to mark all substrings that contain at least k of that character without overcounting?
        
        # Actually, we can use a two-pointer method to find, for each starting index, the minimal ending index such that the substring from start to end has at least k of each character? No, we need at least one character with k.
        
        # Another idea: for each character, we can find all substrings that have at least k of that character by using a two-pointer and a frequency array. Then, we can store the start and end indices of these substrings. Then, the union of all these substrings (by their start and end) is the answer.
        # But then, we need to avoid storing all substrings because there could be many.
        
        # Alternatively, we can use a set to record the start and end indices of all substrings that are valid. But the total number of valid substrings might be large, but the constraints are n=3000, so worst-case 4.5e6 substrings, which is acceptable in C++ but in Python, storing 4.5e6 tuples (each tuple is two integers) might be around 36 MB, which is acceptable in many cases, but we need to check if the approach is efficient.
        
        # Steps:
        # 1. Initialize an empty set to store valid substrings (as tuples (i, j)).
        # 2. For each starting index i, we can expand j and maintain a frequency array for the substring s[i:j+1]. When for any character, the frequency reaches k, then all substrings starting at i and ending from j to the end of the string (or until the condition breaks) are valid? Actually, once a substring has a character with frequency >=k, then extending it will keep that character's frequency >=k, so all substrings starting at i and ending from j to n-1 are valid. But wait, that's not true because if we extend, the frequency of that character might stay >=k, but we don't need to check other characters because the condition is at least one character with >=k. So, once we have at least one character with >=k, then the substring is valid, and any extension is also valid. But also, we can have multiple characters reaching k at different points. But once one character reaches k, then the substring is valid and remains valid for all longer substrings starting at i.
        # 3. So, for each starting index i, we can find the minimal j such that the substring s[i:j+1] has at least one character with frequency >=k. Then, all substrings starting at i and ending from j to n-1 are valid. Then, we can add (n - j) to the count (because from j to n-1, there are n - j substrings starting at i). But wait, we must ensure that we don't count the same substring multiple times if it is valid for multiple characters? Actually, no, because we are counting by starting index and then the minimal j. But the same substring might be counted multiple times if it is valid for multiple characters? Actually, no, because we are counting each substring only once: for each starting index i, we find the minimal j (let's call it j_min) such that the substring from i to j_min has at least one character with frequency >=k. Then, we count all substrings from i to j_min, i to j_min+1, ... i to n-1. This way, each substring is counted exactly once: when we start at its starting index and find the minimal j for which the condition is met. But wait, what if a substring is valid because of two different characters? Then, we might count it twice: once for each character that first reaches k in that substring