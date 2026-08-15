import re

def _format_java_float(value):
    if value != value:
        return "NaN"
    if value == float('inf'):
        return "Infinity"
    if value == float('-inf'):
        return "-Infinity"
    return "{:.3f}".format(value)

class BinaryDataProcessor:
    def __init__(self, binaryString):
        self.binaryString = binaryString
        self.cleanNonBinaryChars()

    def cleanNonBinaryChars(self):
        self.binaryString = re.sub(r'[^01]', '', self.binaryString)

    def calculateBinaryInfo(self):
        zeroesCount = len(self.binaryString) - len(self.binaryString.replace("0", ""))
        onesCount = len(self.binaryString) - len(self.binaryString.replace("1", ""))
        totalLength = len(self.binaryString)

        zeroesPercentage = self._safe_divide(zeroesCount, totalLength)
        onesPercentage = self._safe_divide(onesCount, totalLength)

        return BinaryInfo(zeroesPercentage, onesPercentage, totalLength)

    @staticmethod
    def _safe_divide(numerator, denominator):
        if denominator == 0:
            if numerator == 0:
                return float('nan')
            elif numerator > 0:
                return float('inf')
            else:
                return float('-inf')
        return numerator / denominator

    def convertToAscii(self):
        asciiString = []
        for i in range(0, len(self.binaryString), 8):
            if i + 8 > len(self.binaryString):
                raise IndexError("begin {}, end {}, length {}".format(i, i + 8, len(self.binaryString)))
            byteString = self.binaryString[i:i + 8]
            decimal = int(byteString, 2)
            asciiString.append(chr(decimal))
        return ''.join(asciiString)

    def convertToUtf8(self):
        utf8String = []
        for i in range(0, len(self.binaryString), 8):
            if i + 8 > len(self.binaryString):
                raise IndexError("begin {}, end {}, length {}".format(i, i + 8, len(self.binaryString)))
            byteString = self.binaryString[i:i + 8]
            decimal = int(byteString, 2)
            utf8String.append(chr(decimal))
        return ''.join(utf8String)

    def getBinaryString(self):
        return self.binaryString


class BinaryInfo:
    def __init__(self, zeroes, ones, bitLength):
        self.zeroes = zeroes
        self.ones = ones
        self.bitLength = bitLength

    def getZeroes(self):
        return self.zeroes

    def getOnes(self):
        return self.ones

    def getBitLength(self):
        return self.bitLength

    def __str__(self):
        return "{Zeroes: {}, Ones: {}, Bit length: {}}".format(
            _format_java_float(self.zeroes),
            _format_java_float(self.ones),
            self.bitLength
        )


if __name__ == "__main__":
    bdp = BinaryDataProcessor("0110100001100101011011000110110001101111")
    print(bdp.getBinaryString())
    print(bdp.calculateBinaryInfo())
    print(bdp.convertToAscii())
    print(bdp.convertToUtf8())