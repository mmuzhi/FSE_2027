class NumberWordFormatter:
    NUMBER = ["", "ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE"]
    NUMBER_TEEN = ["TEN", "ELEVEN", "TWELVE", "THIRTEEN", "FOURTEEN", "FIFTEEN", "SIXTEEN", "SEVENTEEN", "EIGHTEEN", "NINETEEN"]
    NUMBER_TEN = ["TEN", "TWENTY", "THIRTY", "FORTY", "FIFTY", "SIXTY", "SEVENTY", "EIGHTY", "NINETY"]
    NUMBER_MORE = ["", "THOUSAND", "MILLION", "BILLION"]
    NUMBER_SUFFIX = ["k", "w", "", "m", "", "", "b", "", "", "t", "", "", "p", "", "", "e"]

    def format(self, x):
        if x is None:
            return ""
        return self.formatString(str(x))

    def formatString(self, x):
        parts = x.split(".")
        lstr = parts[0]
        rstr = parts[1] if len(parts) > 1 else ""
        lstrrev = lstr[::-1]

        if len(lstrrev) % 3 == 1:
            lstrrev += "00"
        elif len(lstrrev) % 3 == 2:
            lstrrev += "0"

        lm = ""
        for i in range(len(lstrrev) // 3):
            chunk = lstrrev[3 * i:3 * i + 3][::-1]
            if chunk != "000":
                lm = self.transThree(chunk) + " " + self.parseMore(i) + " " + lm
            else:
                lm = self.transThree(chunk) + lm

        xs = "AND CENTS " + self.transTwo(rstr) + " " if rstr else ""
        if lm.strip() == "":
            return "ZERO ONLY"
        else:
            return lm.strip() + " " + xs + "ONLY"

    def transTwo(self, s):
        s = s.rjust(2).replace(' ', '0')
        if s[0] == '0':
            return self.NUMBER[int(s[1:])]
        elif s[0] == '1':
            return self.NUMBER_TEEN[int(s) - 10]
        elif s[1] == '0':
            return self.NUMBER_TEN[int(s[0]) - 1]
        else:
            return self.NUMBER_TEN[int(s[0]) - 1] + " " + self.NUMBER[int(s[1:])]

    def transThree(self, s):
        if s[0] == '0':
            return self.transTwo(s[1:])
        elif s[1:] == "00":
            return self.NUMBER[int(s[0])] + " HUNDRED"
        else:
            return self.NUMBER[int(s[0])] + " HUNDRED AND " + self.transTwo(s[1:])

    def parseMore(self, i):
        return self.NUMBER_MORE[i]