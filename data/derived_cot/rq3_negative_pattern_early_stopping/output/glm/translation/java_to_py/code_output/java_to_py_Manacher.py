class Manacher:
    def __init__(self, input_string):
        self.input_string = input_string

    def _preprocess(self, s):
        sb = []
        for i in range(len(s)):
            sb.append('|')
            sb.append(s[i])
        sb.append('|')
        return ''.join(sb)

    def _palindromic_length(self, s, center):
        diff = 1
        while (center - diff >= 0
               and center + diff < len(s)
               and s[center - diff] == s[center + diff]):
            diff += 1
        return diff - 1

    def palindromic_string(self):
        processed_string = self._preprocess(self.input_string)
        max_length = 0
        center_index = 0

        for i in range(len(processed_string)):
            length = self._palindromic_length(processed_string, i)
            if length > max_length:
                max_length = length
                center_index = i

        result = processed_string[center_index - max_length:center_index + max_length + 1]
        return result.replace("|", "")


if __name__ == "__main__":
    manacher = Manacher("ababaxse")
    print(manacher.palindromic_string())