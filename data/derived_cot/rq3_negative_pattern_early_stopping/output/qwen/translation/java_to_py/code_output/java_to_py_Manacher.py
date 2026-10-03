class Manacher:
    def __init__(self, input_string):
        self.input_string = input_string

    def preprocess(self, s):
        return '|' + '|'.join(s) + '|'

    def palindromicLength(self, s, center):
        n = len(s)
        diff = 1
        while center - diff >= 0 and center + diff < n and s[center - diff] == s[center + diff]:
            diff += 1
        return diff - 1

    def palindromicString(self):
        processed_string = self.preprocess(self.input_string)
        max_length = 0
        center_index = 0

        for i in range(len(processed_string)):
            length = self.palindromicLength(processed_string, i)
            if length > max_length:
                max_length = length
                center_index = i

        start = center_index - max_length
        end = center_index + max_length + 1
        result = processed_string[start:end]
        return result.replace('|', '')

if __name__ == '__main__':
    manacher = Manacher("ababaxse")
    print(manacher.palindromicString())