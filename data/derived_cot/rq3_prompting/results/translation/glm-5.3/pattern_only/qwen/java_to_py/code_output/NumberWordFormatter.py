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
        # Java's split drops trailing empty strings (only when a match occurred)
        if "." in x:
            while parts and parts[-1] == "":
                parts.pop()
        lstr = parts[0]
        rstr = parts[1] if len(parts) > 1 else ""
        lstrrev = lstr[::-1]
        a = [None] * 5

        if len(lstrrev) % 3 == 1:
            lstrrev += "00"
        elif len(lstrrev) % 3 == 2:
            lstrrev += "0"

        lm = ""
        for i in range(len(lstrrev) // 3):
            a[i] = lstrrev[3 * i:3 * i + 3][::-1]
            if a[i] != "000":
                lm = self.transThree(a[i]) + " " + self.parseMore(i) + " " + lm
            else:
                lm = self.transThree(a[i]) + lm

        xs = ("AND CENTS " + self.transTwo(rstr) + " ") if rstr != "" else ""
        if lm.strip() == "":
            return "ZERO ONLY"
        else:
            return lm.strip() + " " + xs + "ONLY"

    def transTwo(self, s):
        s = ("%2s" % s).replace(" ", "0")
        if s[0] == "0":
            return self._get(self.NUMBER, int(s[1:]))
        elif s[0] == "1":
            return self._get(self.NUMBER_TEEN, int(s) - 10)
        elif s[1] == "0":
            return self._get(self.NUMBER_TEN, int(s[0:1]) - 1)
        else:
            return self._get(self.NUMBER_TEN, int(s[0:1]) - 1) + " " + self._get(self.NUMBER, int(s[1:]))

    def transThree(self, s):
        if s[0] == "0":
            return self.transTwo(s[1:])
        elif s[1:] == "00":
            return self._get(self.NUMBER, int(s[0:1])) + " HUNDRED"
        else:
            return self._get(self.NUMBER, int(s[0:1])) + " HUNDRED AND " + self.transTwo(s[1:])

    def parseMore(self, i):
        return self._get(self.NUMBER_MORE, i)

    @staticmethod
    def _get(arr, idx):
        # Java-style array access: negative indices must not wrap around
        if idx < 0 or idx >= len(arr):
            raise IndexError("Index %d out of bounds for length %d" % (idx, len(arr)))
        return arr[idx]