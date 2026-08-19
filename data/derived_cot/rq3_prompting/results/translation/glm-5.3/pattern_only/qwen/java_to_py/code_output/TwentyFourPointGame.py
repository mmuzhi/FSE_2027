import random


class TwentyFourPointGame:
    def __init__(self):
        self.nums = self.get_my_cards()

    def get_my_cards(self):
        cards = []
        for _ in range(4):
            cards.append(random.randint(1, 9))
        return cards

    def answer(self, expression):
        if expression == "pass":
            self.nums = self.get_my_cards()
            return False

        counts = [0] * 10
        for c in expression:
            if c.isdecimal():  # matches Java's Character.isDigit (Nd category)
                counts[int(c)] += 1

        for num in self.nums:
            if counts[num] > 0:
                counts[num] -= 1
            else:
                return False

        for count in counts:
            if count != 0:
                return False

        return self.evaluate_expression(expression)

    def evaluate_expression(self, expression):
        pos = -1
        ch = -1

        def next_char():
            nonlocal pos, ch
            pos += 1
            ch = ord(expression[pos]) if pos < len(expression) else -1

        def eat(char_to_eat):
            while ch == 32:  # ' '
                next_char()
            if ch == char_to_eat:
                next_char()
                return True
            return False

        def parse():
            nonlocal pos
            next_char()
            x = parse_expression()
            if pos < len(expression):
                raise ValueError("Unexpected: " + chr(ch) if ch != -1 else "Unexpected: ")
            return x

        def parse_expression():
            x = parse_term()
            while True:
                if eat(43):  # '+'
                    x += parse_term()
                elif eat(45):  # '-'
                    x -= parse_term()
                else:
                    return x

        def parse_term():
            x = parse_factor()
            while True:
                if eat(42):  # '*'
                    x *= parse_factor()
                elif eat(47):  # '/'
                    x /= parse_factor()
                else:
                    return x

        def parse_factor():
            nonlocal pos
            if eat(43):  # '+'
                return parse_factor()
            if eat(45):  # '-'
                return -parse_factor()

            x = 0.0
            start_pos = pos
            if eat(40):  # '('
                x = parse_expression()
                eat(41)  # ')'
            elif (48 <= ch <= 57) or ch == 46:  # '0'-'9' or '.'
                while (48 <= ch <= 57) or ch == 46:
                    next_char()
                x = float(expression[start_pos:pos])
            else:
                raise ValueError("Unexpected: " + (chr(ch) if ch != -1 else ""))

            return x

        try:
            return parse() == 24
        except Exception:
            return False

    def get_nums(self):
        return self.nums