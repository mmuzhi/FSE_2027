import random
import math
import unicodedata


class TwentyFourPointGame:
    def __init__(self):
        self.nums = self.getMyCards()

    def getMyCards(self):
        return [random.randint(1, 9) for _ in range(4)]

    def answer(self, expression):
        if expression == "pass":
            self.nums = self.getMyCards()
            return False

        counts = [0] * 10
        for c in expression:
            if c.isdecimal():
                counts[unicodedata.decimal(c, -1)] += 1

        for num in self.nums:
            if counts[num] > 0:
                counts[num] -= 1
            else:
                return False

        for count in counts:
            if count != 0:
                return False

        return self.evaluateExpression(expression)

    def evaluateExpression(self, expression):
        try:
            pos = -1
            ch = -1

            def next_char():
                nonlocal pos, ch
                pos += 1
                ch = ord(expression[pos]) if pos < len(expression) else -1

            def eat(char_to_eat):
                while ch == ord(' '):
                    next_char()
                if ch == char_to_eat:
                    next_char()
                    return True
                return False

            def parse_factor():
                nonlocal pos, ch
                if eat(ord('+')):
                    return parse_factor()
                if eat(ord('-')):
                    return -parse_factor()

                start_pos = pos
                if eat(ord('(')):
                    x = parse_expression()
                    eat(ord(')'))
                    return x
                elif (ch >= ord('0') and ch <= ord('9')) or ch == ord('.'):
                    while (ch >= ord('0') and ch <= ord('9')) or ch == ord('.'):
                        next_char()
                    return float(expression[start_pos:pos])
                else:
                    raise RuntimeError(
                        "Unexpected: " + chr(ch) if ch != -1 else "Unexpected: EOF"
                    )

            def safe_div(a, b):
                if b == 0:
                    if a == 0:
                        return float('nan')
                    sign = math.copysign(1.0, a) * math.copysign(1.0, b)
                    return sign * float('inf')
                return a / b

            def parse_term():
                x = parse_factor()
                while True:
                    if eat(ord('*')):
                        x *= parse_factor()
                    elif eat(ord('/')):
                        x = safe_div(x, parse_factor())
                    else:
                        return x

            def parse_expression():
                x = parse_term()
                while True:
                    if eat(ord('+')):
                        x += parse_term()
                    elif eat(ord('-')):
                        x -= parse_term()
                    else:
                        return x

            def parse():
                nonlocal pos, ch
                next_char()
                x = parse_expression()
                if pos < len(expression):
                    raise RuntimeError(
                        "Unexpected: " + chr(ch) if ch != -1 else "Unexpected: EOF"
                    )
                return x

            return parse() == 24
        except Exception:
            return False

    def getNums(self):
        return self.nums