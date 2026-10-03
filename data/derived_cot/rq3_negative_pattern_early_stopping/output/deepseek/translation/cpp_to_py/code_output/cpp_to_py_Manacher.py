class Manacher:
    def __init__(self, input_string: str):
        self.input_string = input_string

    def palindromic_length(self, center: int, diff: int, s: str) -> int:
        if (center - diff == -1) or (center + diff == len(s)) or (s[center - diff] != s[center + diff]):
            return 0
        return 1 + self.palindromic_length(center, diff + 1, s)

    def palindromic_string(self) -> str:
        max_length = 0
        new_input_string = ""
        output_string = ""

        for i in range(len(self.input_string) - 1):
            new_input_string += self.input_string[i] + "|"
        new_input_string += self.input_string[-1]

        start = 0
        for i in range(len(new_input_string)):
            length = self.palindromic_length(i, 1, new_input_string)

            if max_length < length:
                max_length = length
                start = i

        for i in range(start - max_length, start + max_length + 1):
            if new_input_string[i] != '|':
                output_string += new_input_string[i]

        return output_string