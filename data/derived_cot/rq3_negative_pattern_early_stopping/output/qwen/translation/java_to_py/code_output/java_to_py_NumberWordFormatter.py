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
        parts = x.split('.')
        lstr = parts[0]
        rstr = parts[1] if len(parts) > 1 else ""
        
        if not lstr:
            return "ZERO " + ("AND CENTS " + self.transTwo(rstr) + " " if rstr else "ONLY")
        
        lstr_rev = lstr[::-1]
        if len(lstr_rev) % 3 == 1:
            lstr_rev += '00'
        elif len(lstr_rev) % 3 == 2:
            lstr_rev += '0'
        
        chunks = [lstr_rev[i:i+3][::-1] for i in range(0, len(lstr_rev), 3)]
        result = []
        
        for idx, chunk in enumerate(chunks):
            if chunk != '000':
                word = self.transThree(chunk)
                if word:
                    result.insert(0, word + " " + self.NUMBER_MORE[idx])
        
        integer_part = ' '.join(result).strip()
        cents_part = " AND CENTS " + self.transTwo(rstr) if rstr else ""
        return integer_part + " " + cents_part + "ONLY" if integer_part else "ZERO ONLY"
    
    def transTwo(self, s):
        s = s.zfill(2)
        if s[0] == '0':
            return self.NUMBER[int(s[1])]
        elif s[0] == '1':
            return self.NUMBER_TEEN[int(s[1]) - 1]
        elif s[1] == '0':
            return self.NUMBER_TEN[int(s[0]) - 1]
        else:
            return self.NUMBER_TEN[int(s[0]) - 1] + " " + self.NUMBER[int(s[1])]
    
    def transThree(self, s):
        if s[0] == '0':
            return self.transTwo(s[1:])
        elif s[1:] == '00':
            return self.NUMBER[int(s[0])] + " HUNDRED"
        else:
            return self.NUMBER[int(s[0])] + " HUNDRED AND " + self.transTwo(s[1:])