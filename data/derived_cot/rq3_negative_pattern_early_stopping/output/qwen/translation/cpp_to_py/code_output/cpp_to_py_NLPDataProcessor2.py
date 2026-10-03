import re
import locale

# Set the locale to the system default to match C++ behavior
locale.setlocale(locale.LC_CTYPE, '')  # This might throw an error if the locale is not set

def to_lowercase(str):
    return str.lower()

def remove_non_alpha(str):
    result = []
    for c in str:
        # Check using the current locale
        if locale.isspace(c) or locale.isalpha(c):
            result.append(c)
    return ''.join(result)

class NLPDataProcessor2:
    # We'll use a class-level dictionary for first_appear
    first_appear = {}

    @classmethod
    def calculate_word_frequency(cls, words_list):
        # Clear the first_appear dictionary at the beginning of the method
        cls.first_appear.clear()
        word_frequency = {}
        js = 0  # This is a counter for first appearance

        for words in words_list:
            for word in words:
                if word not in word_frequency:
                    cls.first_appear[word] = ++js  # Note: in C++ we do ++js then assign, but in Python we can do:
                    # Actually, the C++ code does: first_appear[word] = ++js; which is post-increment? No, it's pre-increment.
                    # Let me check: in C++, `++js` is pre-increment. But note: the code is `++js` and then assign. So it increments js and then assigns.
                    # In Python, we can do: js += 1 and then assign the new value.
                    # But note: the C++ code does: first_appear[word] = ++js; which is equivalent to:
                    #   js = js + 1;
                    #   first_appear[word] = js;
                    # So we do:
                    js += 1
                    cls.first_appear[word] = js
                word_frequency[word] += 1

        # Now, create a list of tuples (word, frequency) and sort
        sorted_word_frequency = sorted(word_frequency.items(), key=lambda x: (-x[1], cls.first_appear[x[0]]))
        # But note: the C++ comparator: 
        #   if frequencies are equal, then compare by first_appear (the order of first occurrence). 
        #   In C++, the comparator returns true if a should come before b. 
        #   In the C++ code: 
        #       if (a.second == b.second) { return first_appear[a.first] < first_appear[b.first]; }
        #       else { return b.second < a.second; }
        #   This means: 
        #       if frequencies are equal, then sort by first_appear (ascending, i.e., lower first_appear comes first)
        #       else, sort by frequency (descending, because if b.second < a.second then a comes before b, meaning higher frequency first)
        #
        # In Python, we can do:
        #   sorted_word_frequency = sorted(word_frequency.items(), key=lambda x: (-x[1], cls.first_appear[x[0]]))
        #   This sorts by frequency descending (because of the negative) and then by first_appear ascending (because the second key is the first_appear value, and we don't negate it).
        #
        # But note: the C++ code does not negate the frequency. We are using negative to get descending order. Alternatively, we can do:
        #   sorted_word_frequency = sorted(word_frequency.items(), key=lambda x: (x[1], cls.first_appear[x[0]]), reverse=True)
        #   But that would sort by frequency descending and then by first_appear descending? No, because the second key is not negated.
        #
        # Actually, the C++ comparator does:
        #   if (a.second == b.second) {
        #       return first_appear[a.first] < first_appear[b.first];
        #   } else {
        #       return b.second < a.second;
        #   }
        #
        # This is equivalent to:
        #   primary key: frequency (descending)
        #   secondary key: first_appear (ascending)
        #
        # We can do in Python:
        #   sorted_word_frequency = sorted(word_frequency.items(), key=lambda x: (-x[1], cls.first_appear[x[0]]))
        #
        # But note: the C++ code does not use negative for frequency. We are using negative to get descending order. Alternatively, we can do:
        #   sorted_word_frequency = sorted(word_frequency.items(), key=lambda x: (x[1], cls.first_appear[x[0]]), reverse=True)
        #   This would sort by frequency descending and then by first_appear descending? Because reverse=True reverses both keys.
        #
        # We don't want that. We want frequency descending and first_appear ascending.
        #
        # So we do:
        #   sorted_word_frequency = sorted(word_frequency.items(), key=lambda x: (-x[1], cls.first_appear[x[0]]))
        #
        # But note: the C++ code does not use negative. We are using negative to get descending order for frequency. This is acceptable because we want higher frequency first.
        #
        # However, the C++ code does not use negative. We are allowed to change the behavior if we use idiomatic Python? The problem says: "Use idiomatic Python only when it doesn't change behavior." 
        #   Using negative for frequency is a common trick and does not change the behavior (it's just a different way to achieve the same order).
        #
        # So we'll keep the negative for frequency.

        # Now, take the top 5
        top_5_word_frequency = {}
        for i in range(min(5, len(sorted_word_frequency))):
            word, count = sorted_word_frequency[i]
            top_5_word_frequency[word] = count

        return top_5_word_frequency

    @classmethod
    def process(cls, string_list):
        words_list = cls.process_data(string_list)
        return cls.calculate_word_frequency(words_list)

    @classmethod
    def process_data(cls, string_list):
        words_list = []
        word_regex = r'\s+'

        for str in string_list:
            processed_string = to_lowercase(remove_non_alpha(str))
            # Now split the string by one or more whitespaces
            words = re.split(word_regex, processed_string)
            # Remove empty strings
            words = [word for word in words if word]
            words_list.append(words)

        return words_list