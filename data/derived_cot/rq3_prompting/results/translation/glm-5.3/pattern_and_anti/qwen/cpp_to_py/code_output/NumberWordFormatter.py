class NumberWordFormatter:
    def __init__(self):
        self.NUMBER = ["", "ONE", "TWO", "THREE", "FOUR", "FIVE",
                       "SIX", "SEVEN", "EIGHT", "NINE"]
        self.NUMBER_TEEN = ["TEN", "ELEVEN", "TWELVE", "THIRTEEN", "FOURTEEN",
                            "FIFTEEN", "SIXTEEN", "SEVENTEEN", "EIGHTEEN", "NINETEEN"]
        self.NUMBER_TEN = ["TEN", "TWENTY", "THIRTY", "FORTY", "FIFTY",
                           "SIXTY", "SEVENTY", "EIGHTY", "NINETY"]
        self.NUMBER_MORE = ["", "THOUSAND", "MILLION", "BILLION"]
        self.NUMBER_SUFFIX = ["k", "w", "", "m", "", "", "b", "", "",
                              "t", "", "", "p", "", "", "e"]

    def format(self, x=None):
        # Overload dispatch: format(int) / format(double) / format(str) / format(nullptr_t)
        if x is None:
            return ""
        if isinstance(x, str):
            return self._format_str(x)
        if isinstance(x, bool):  # C++ promotes bool to int
            return self._format_str(str(int(x)))
        if isinstance(x, int):
            return self._format_str(str(x))
        if isinstance(x, float):
            # C++ stringstream default: 6 significant digits, %g-style formatting
            return self._format_str("%g" % x)
        raise TypeError("NumberWordFormatter.format(): unsupported argument type")

    def _format_str(self, x):
        dot = x.find('.')
        lstr = x[:dot] if dot != -1 else x  # substr(0, npos) == whole string
        rstr = x[dot + 1:] if dot != -1 else ""
        lstr = lstr[::-1]

        if len(lstr) % 3 == 1:
            lstr += "00"
        elif len(lstr) % 3 == 2:
            lstr += "0"

        lm = ""
        for i in range(len(lstr) // 3):
            a = lstr[3 * i + 2] + lstr[3 * i + 1] + lstr[3 * i]
            if a != "000":
                lm = self.trans_three(a) + " " + self.parse_more(i) + " " + lm
            else:
                lm += self.trans_three(a)

        xs = "AND CENTS " + self.trans_two(rstr) + " " if rstr != "" else ""
        if lm == "":
            return "ZERO ONLY"
        nowpos = 0
        for i in range(len(lm) - 1, -1, -1):
            if lm[i] != ' ':
                nowpos = i
                break
        lm = lm[:nowpos + 1]
        return lm + " " + xs + "ONLY"

    def trans_two(self, s):
        ss = s
        if len(ss) == 1:
            ss = "0" + ss
        if ss[0] == '0':
            return self.NUMBER[ord(ss[1]) - ord('0')]
        elif ss[0] == '1':
            return self.NUMBER_TEEN[int(ss) - 10]
        elif ss[1] == '0':
            return self.NUMBER_TEN[ord(ss[0]) - ord('1')]
        else:
            return self.NUMBER_TEN[ord(ss[0]) - ord('1')] + " " + self.NUMBER[ord(ss[1]) - ord('0')]

    def trans_three(self, s):
        if s[0] == '0':
            return self.trans_two(s[1:])
        elif s[1:] == "00":
            return self.NUMBER[ord(s[0]) - ord('0')] + " HUNDRED"
        else:
            return self.NUMBER[ord(s[0]) - ord('0')] + " HUNDRED AND " + self.trans_two(s[1:])

    def parse_more(self, i):
        return self.NUMBER_MORE[i]