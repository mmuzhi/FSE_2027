class Manacher:
    def __init__(self, input_string):
        self.input_string = input_string

    def preprocess(self, s):
        return "|" + "|".join(s) + "|"

    def palindromicLength(self, s, center):
        diff = 1
        while (center - diff >= 0 and center + diff < len(s) and
               s[center - diff] == s[center + diff]):
            diff += 1
        return diff - 1

    def palindromicString(self):
        processed = self.preprocess(self.input_string)
        max_length = 0
        center_index = 0

        for i in range(len(processed)):
            length = self.palindromicLength(processed, i)
            if length > max_length:
                max_length = length
                center_index = i

        result = processed[center_index - max_length: center_index + max_length + 1]
        return result.replace("|", "")

if __name__ == "__main__":
    manacher = Manacher("ababaxse")
    print(manacher.palindromicString())