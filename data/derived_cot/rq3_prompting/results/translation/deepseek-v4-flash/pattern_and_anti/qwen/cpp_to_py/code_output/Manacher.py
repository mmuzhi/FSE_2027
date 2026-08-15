class Manacher:
    def __init__(self, input_string):
        self.input_string = input_string

    def palindromic_length(self, center, diff, str):
        length = 0
        while True:
            if center - diff == -1 or center + diff == len(str) or str[center - diff] != str[center + diff]:
                return length
            length += 1
            diff += 1

    def palindromic_string(self):
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