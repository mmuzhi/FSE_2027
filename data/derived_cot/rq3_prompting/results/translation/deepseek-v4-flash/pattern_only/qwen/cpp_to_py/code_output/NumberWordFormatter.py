class NumberWordFormatter:
    NUMBER = ["", "ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE"]
    NUMBER_TEEN = ["TEN", "ELEVEN", "TWELVE", "THIRTEEN", "FOURTEEN", "FIFTEEN", "SIXTEEN", "SEVENTEEN", "EIGHTEEN", "NINETEEN"]
    NUMBER_TEN = ["TEN", "TWENTY", "THIRTY", "FORTY", "FIFTY", "SIXTY", "SEVENTY", "EIGHTY", "NINETY"]
    NUMBER_MORE = ["", "THOUSAND", "MILLION", "BILLION"]
    NUMBER_SUFFIX = ["k", "w", "", "m", "", "", "b", "", "", "t", "", "", "p", "", "", "e", "", "", "", "", ""]

    def __init__(self):
        pass

    def format(self, x):
        if x is None:
            return ""
        if isinstance(x, bool):
            return self.format(str(int(x)))
        if isinstance(x, int):
            return self.format(str(x))
        if isinstance(x, float):
            return self.format('{:.6g}'.format(x))
        if isinstance(x, str):
            return self._format_string(x)
        raise TypeError("Unsupported type")

    def _format_string(self, x):
        dot = x.find('.')
        if dot == -1:
            lstr = x
            rstr = ""
        else:
            lstr = x[:dot]
            rstr = x[dot + 1:]

        lstr = lstr[::-1]

        if len(lstr) % 3 == 1:
            lstr += "00"
        elif len(lstr) % 3 == 2:
            lstr += "0"

        a = [""] * 5
        lm = ""

        for i in range(len(lstr) // 3):
            a[i] = lstr[3 * i + 2] + lstr[3 * i + 1] + lstr[3 * i]
            if a[i] != "000":
                lm = self.trans_three(a[i]) + " " + self.parse_more(i) + " " + lm
            else:
                lm += self.trans_three(a[i])

        xs = ""
        if rstr:
            xs = "AND CENTS " + self.trans_two(rstr) + " "

        if lm == "":
            return "ZERO ONLY"
        else:
            lm = lm.rstrip(' ')
            return lm + " " + xs + "ONLY"

    def trans_two(self, s):
        ss = s
        if len(ss) == 1:
            ss = "0" + ss
        if ss[0] == '0':
            return self.NUMBER[int(ss[1])]
        elif ss[0] == '1':
            return self.NUMBER_TEEN[int(ss) - 10]
        elif ss[1] == '0':
            return self.NUMBER_TEN[int(ss[0]) - 1]
        else:
            return self.NUMBER_TEN[int(ss[0]) - 1] + " " + self.NUMBER[int(ss[1])]

    def trans_three(self, s):
        if s[0] == '0':
            return self.trans_two(s[1:])
        elif s[1:] == "00":
            return self.NUMBER[int(s[0])] + " HUNDRED"
        else:
            return self.NUMBER[int(s[0])] + " HUNDRED AND " + self.trans_two(s[1:])

    def parse_more(self, i):
        return self.NUMBER_MORE[i]