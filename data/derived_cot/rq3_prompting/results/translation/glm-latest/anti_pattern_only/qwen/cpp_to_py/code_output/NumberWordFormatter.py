class NumberWordFormatter:
    NUMBER = ("", "ONE", "TWO", "THREE", "FOUR", "FIVE",
              "SIX", "SEVEN", "EIGHT", "NINE")
    NUMBER_TEEN = ("TEN", "ELEVEN", "TWELVE", "THIRTEEN", "FOURTEEN",
                   "FIFTEEN", "SIXTEEN", "SEVENTEEN", "EIGHTEEN", "NINETEEN")
    NUMBER_TEN = ("TEN", "TWENTY", "THIRTY", "FORTY", "FIFTY",
                  "SIXTY", "SEVENTY", "EIGHTY", "NINETY")
    NUMBER_MORE = ("", "THOUSAND", "MILLION", "BILLION")
    NUMBER_SUFFIX = ("k", "w", "", "m", "", "", "b", "", "",
                     "t", "", "", "p", "", "", "e")

    def format(self, x=None):
        # Replaces the C++ overloads: format(int), format(double),
        # format(const std::string&), format(std::nullptr_t)
        if x is None:
            return ""
        if isinstance(x, bool):
            x = int(x)
        if isinstance(x, int):
            return self._format_string(str(x))
        elif isinstance(x, float):
            # std::stringstream's default double formatting is equivalent
            # to '%g' (6 significant digits, strips trailing zeros).
            return self._format_string('%g' % x)
        else:
            return self._format_string(x)

    def _format_string(self, x):
        pos = x.find('.')
        lstr = x[:pos] if pos != -1 else x
        rstr = x[pos + 1:] if pos != -1 else ''
        lstr = lstr[::-1]

        if len(lstr) % 3 == 1:
            lstr += "00"
        elif len(lstr) % 3 == 2:
            lstr += "0"

        a = ["", "", "", "", ""]
        lm = ""

        for i in range(len(lstr) // 3):
            a[i] = lstr[3 * i + 2] + lstr[3 * i + 1] + lstr[3 * i]

            if a[i] != "000":
                lm = self.trans_three(a[i]) + " " + self.parse_more(i) + " " + lm
            else:
                lm += self.trans_three(a[i])

        xs = "AND CENTS " + self.trans_two(rstr) + " " if rstr else ""
        if not lm:
            return "ZERO ONLY"
        else:
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