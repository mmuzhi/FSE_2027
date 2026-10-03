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
        parts = x.split(".")
        lstr = parts[0]
        rstr = parts[1] if len(parts) > 1 else ""
        lstrrev = lstr[::-1]
        a = [""] * 5

        if len(lstrrev) % 3 == 1:
            lstrrev += "00"
        elif len(lstrrev) % 3 == 2:
            lstrrev += "0"

        lm = []
        for i in range(len(lstrrev) // 3):
            a[i] = lstrrev[3 * i:3 * i + 3][::-1]
            if a[i] != "000":
                lm.insert(0, self.trans_three(a[i]) + " " + self.parse_more(i) + " ")
            else:
                lm.insert(0, self.trans_three(a[i]))

        xs = ""
        if rstr:
            xs = "AND CENTS " + self.trans_two(rstr) + " "
        lm_str = "".join(lm).strip()
        if not lm_str:
            return "ZERO ONLY"
        else:
            return lm_str + " " + xs + "ONLY"

    def trans_two(self, s):
        s = s.zfill(2)
        if s[0] == '0':
            return self.NUMBER[int(s[1])]
        elif s[0] == '1':
            return self.NUMBER_TEEN[int(s) - 10]
        elif s[1] == '0':
            return self.NUMBER_TEN[int(s[0]) - 1]
        else:
            return self.NUMBER_TEN[int(s[0]) - 1] + " " + self.NUMBER[int(s[1])]

    def trans_three(self, s):
        if s[0] == '0':
            return self.trans_two(s[1:])
        elif s[1:] == "00":
            return self.NUMBER[int(s[0])] + " HUNDRED"
        else:
            return self.NUMBER[int(s[0])] + " HUNDRED AND " + self.trans_two(s[1:])

    def parse_more(self, i):
        return self.NUMBER_MORE[i]