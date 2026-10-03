class BinaryDataProcessor:
    def __init__(self, binary_string):
        self.binary_string = binary_string
        self.cleanNonBinaryChars()

    def cleanNonBinaryChars(self):
        self.binary_string = ''.join(filter(str.isalnum, self.binary_string))
        # Alternatively, we can use: 
        # self.binary_string = ''.join(c for c in self.binary_string if c in '01')

    def calculateBinaryInfo(self):
        total_length = len(self.binary_string)
        zeroes_count = total_length - len(self.binary_string.replace('0', ''))
        ones_count = total_length - len(self.binary_string.replace('1', ''))
        zeroes_percentage = zeroes_count / total_length
        ones_percentage = ones_count / total_length
        return BinaryInfo(zeroes_percentage, ones_percentage, total_length)

    def convertToAscii(self):
        result = []
        for i in range(0, len(self.binary_string), 8):
            byte_str = self.binary_string[i:i+8]
            if byte_str:
                decimal = int(byte_str, 2)
                result.append(chr(decimal))
        return ''.join(result)

    def convertToUtf8(self):
        result = []
        for i in range(0, len(self.binary_string), 8):
            byte_str = self.binary_string[i:i+8]
            if byte_str:
                decimal = int(byte_str, 2)
                result.append(chr(decimal))
        return ''.join(result)

    def getBinaryString(self):
        return self.binary_string

class BinaryInfo:
    def __init__(self, zeroes, ones, bitLength):
        self.zeroes = zeroes
        self.ones = ones
        self.bitLength = bitLength

    def __str__(self):
        return f"{{Zeroes: {self.zeroes:.3f}, Ones: {self.ones:.3f}, Bit length: {self.bitLength}}}"

if __name__ == "__main__":
    bdp = BinaryDataProcessor("0110100001100101011011000110110001101111")
    print(bdp.getBinaryString())
    print(bdp.calculateBinaryInfo())
    print(bdp.convertToAscii())
    print(bdp.convertToUtf8())