class Manacher:
    def __init__(self, inputString):
        self.inputString = inputString

    def preprocess(self, s):
        sb = []
        for ch in s:
            sb.append('|')
            sb.append(ch)
        sb.append('|')
        return ''.join(sb)

    def palindromicLength(self, s, center):
        diff = 1
        while center - diff >= 0 and center + diff < len(s) and s[center - diff] == s[center + diff]:
            diff += 1
        return diff - 1

    def palindromicString(self):
        processedString = self.preprocess(self.inputString)
        maxLength = 0
        centerIndex = 0

        for i in range(len(processedString)):
            length = self.palindromicLength(processedString, i)
            if length > maxLength:
                maxLength = length
                centerIndex = i

        result = processedString[centerIndex - maxLength: centerIndex + maxLength + 1]
        return result.replace("|", "")


if __name__ == "__main__":
    manacher = Manacher("ababaxse")
    print(manacher.palindromicString())