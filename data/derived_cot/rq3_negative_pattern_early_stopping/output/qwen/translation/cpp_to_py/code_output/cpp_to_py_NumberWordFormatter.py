class NumberWordFormatter:
    def __init__(self):
        self.NUMBER = ["", "ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE"]
        self.NUMBER_TEEN = ["TEN", "ELEVEN", "TWELVE", "THIRTEEN", "FOURTEEN", "FIFTEEN", "SIXTEEN", "SEVENTEEN", "EIGHTEEN", "NINETEEN"]
        self.NUMBER_TEN = ["TEN", "TWENTY", "THIRTY", "FORTY", "FIFTY", "SIXTY", "SEVENTY", "EIGHTY", "NINETY"]
        self.NUMBER_MORE = ["", "THOUSAND", "MILLION", "BILLION"]

    def format(self, x):
        if isinstance(x, int):
            return self.format_int(x)
        elif isinstance(x, float):
            return self.format_double(x)
        elif isinstance(x, str):
            return self.format_string(x)
        elif x is None:
            return self.format_none(x)
        else:
            # If x is of another type, we try to convert to string and then use format_string
            return self.format_string(str(x))

    def format_int(self, x):
        return self.format_string(str(x))

    def format_double(self, x):
        return self.format_string(str(x))

    def format_string(self, x):
        # Split the string into integer part and fractional part
        if '.' in x:
            parts = x.split('.')
            integer_part = parts[0]
            fractional_part = parts[1]
        else:
            integer_part = x
            fractional_part = ""

        # If integer_part is empty, then we have a number less than 1
        if integer_part == "":
            integer_part = "0"

        # Reverse the integer_part
        reversed_str = integer_part[::-1]

        # Pad the reversed_str with zeros to make its length a multiple of 3
        n = len(reversed_str)
        if n % 3 == 1:
            reversed_str += "00"
        elif n % 3 == 2:
            reversed_str += "0"

        # Break into chunks of 3
        chunks = [reversed_str[i:i+3] for i in range(0, len(reversed_str), 3)]

        # Now, process each chunk
        lm = ""
        for i, chunk in enumerate(chunks):
            # Skip if chunk is "000"
            if chunk == "000":
                continue

            # Convert the chunk to words
            chunk_str = self.trans_three(chunk)
            unit = self.parse_more(i)
            if unit != "":
                chunk_str += " " + unit

            # Prepend to lm
            if lm == "":
                lm = chunk_str
            else:
                lm = chunk_str + " " + lm

        # Handle the case when the number is zero
        if lm == "":
            lm = "ZERO"

        # Now, handle the fractional part
        if fractional_part != "":
            # Convert fractional_part to two digits (if needed)
            if len(fractional_part) == 1:
                fractional_part = fractional_part.zfill(2)
            elif len(fractional_part) > 2:
                # In C++, it only takes two digits? But the problem doesn't specify. We'll take the first two.
                fractional_part = fractional_part[:2]

            # Convert to words
            cents = self.trans_two(fractional_part)
            lm += " AND CENTS " + cents
        else:
            # If there's no fractional part, we don't add anything
            pass

        # Add "ONLY" at the end
        lm += " ONLY"

        return lm

    def format_none(self, x):
        return ""

    def trans_two(self, s):
        # s is a string of length 1 or 2
        if len(s) == 1:
            s = "0" + s

        # If the first digit is '0', then it's just the second digit
        if s[0] == '0':
            return self.NUMBER[int(s[1])]

        # If the first digit is '1', then it's a teen
        elif s[0] == '1':
            return self.NUMBER_TEEN[int(s[1])]

        # If the second digit is '0', then it's a ten
        elif s[1] == '0':
            return self.NUMBER_TEN[int(s[0])]

        # Otherwise, it's a ten and a digit
        else:
            return self.NUMBER_TEN[int(s[0])] + " " + self.NUMBER[int(s[1])]

    def trans_three(self, s):
        # s is a string of three digits
        if s[0] == '0':
            # Skip the leading zero
            return self.trans_two(s[1:])

        # If the last two digits are "00", then just the hundreds
        if s[1] == '0' and s[2] == '0':
            return self.NUMBER[int(s[0])] + " HUNDRED"

        # Otherwise, hundreds and the last two digits
        else:
            return self.NUMBER[int(s[0])] + " HUNDRED AND " + self.trans_two(s[1:])

    def parse_more(self, i):
        if i < len(self.NUMBER_MORE):
            return self.NUMBER_MORE[i]
        else:
            # According to the C++ code, the array has 4 elements, so i should be 0,1,2,3.
            # If i is out of bounds, return empty string.
            return ""

# Example usage:
# formatter = NumberWordFormatter()
# print(formatter.format(123.45))  # Should output "ONE HUNDRED AND TWENTY THREE THOUSAND AND CENTS FIVE ONLY"