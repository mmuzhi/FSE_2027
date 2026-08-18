class NumberWordFormatter:
    NUMBER = ["", "ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE"]
    NUMBER_TEEN = ["TEN", "ELEVEN", "TWELVE", "THIRTEEN", "FOURTEEN", "FIFTEEN", "SIXTEEN", "SEVENTEEN", "EIGHTEEN", "NINETEEN"]
    NUMBER_TEN = ["TEN", "TWENTY", "THIRTY", "FORTY", "FIFTY", "SIXTY", "SEVENTY", "EIGHTY", "NINETY"]
    NUMBER_MORE = ["", "THOUSAND", "MILLION", "BILLION"]
    NUMBER_SUFFIX = ["k", "w", "", "m", "", "", "b", "", "", "t", "", "", "p", "", "", "e"]

    def format(self, x):
        if x is None:
            return ""
        return self.format_string(str(x))

    def format_string(self, x):
        # Java split(".") drops trailing empty strings (empty input keeps [""]),
        # e.g. "." -> [] making parts[0] fail; emulate that exactly.
        if x == "":
            parts = [""]
        else:
            parts = x.split(".")
            while parts and parts[-1] == "":
                parts.pop()
        lstr = parts[0]
        rstr = parts[1] if len(parts) > 1 else ""
        lstrrev = lstr[::-1]
        a = [None] * 5  # fixed size like Java: assignment beyond index 4 raises IndexError

        if len(lstrrev) % 3 == 1:
            lstrrev += "00"
        elif len(lstrrev) % 3 == 2:
            lstrrev += "0"

        lm = ""
        for i in range(len(lstrrev) // 3):
            a[i] = lstrrev[3 * i:3 * i + 3][::-1]
            if a[i] != "000":
                lm = self.trans_three(a[i]) + " " + self.parse_more(i) + " " + lm
            else:
                lm = self.trans_three(a[i]) + lm

        xs = "AND CENTS " + self.trans_two(rstr) + " " if rstr != "" else ""
        if lm.strip() == "":
            return "ZERO ONLY"
        else:
            return lm.strip() + " " + xs + "ONLY"

    def trans_two(self, s):
        s = s.rjust(2).replace(" ", "0")  # matches String.format("%2s", s).replace(' ', '0')
        if s[0] == "0":
            return self.NUMBER[int(s[1:])]
        elif s[0] == "1":
            return self.NUMBER_TEEN[int(s) - 10]
        elif s[1] == "0":
            return self.NUMBER_TEN[int(s[0:1]) - 1]
        else:
            return self.NUMBER_TEN[int(s[0:1]) - 1] + " " + self.NUMBER[int(s[1:])]

    def trans_three(self, s):
        if s[0] == "0":
            return self.trans_two(s[1:])
        elif s[1:] == "00":
            return self.NUMBER[int(s[0:1])] + " HUNDRED"
        else:
            return self.NUMBER[int(s[0:1])] + " HUNDRED AND " + self.trans_two(s[1:])

    def parse_more(self, i):
        return self.NUMBER_MORE[i]