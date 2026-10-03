class Solution:
    def countOfSubstrings(self, word: str, k: int) -> int:
        vowels = "aeiou"
        n = len(word)
        count = 0
        for start in range(n):
            vowel_count = [0] * 5
            vowel_total = 0
            all_vowels_found = 0
            for end in range(start, n):
                char = word[end]
                if char in vowels:
                    idx = vowels.index(char)
                    vowel_count[idx] += 1
                    if vowel_count[idx] == 1:
                        all_vowels_found += 1
                    vowel_total += 1
                if all_vowels_found == 5:
                    consonants = (end - start + 1) - vowel_total
                    if consonants == k:
                        count += 1
        return count