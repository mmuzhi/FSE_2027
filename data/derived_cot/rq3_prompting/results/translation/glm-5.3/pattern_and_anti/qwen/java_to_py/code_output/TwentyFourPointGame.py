import random


class TwentyFourPointGame:
    def __init__(self):
        self.nums = self.get_my_cards()

    def get_my_cards(self):
        return [random.randint(1, 9) for _ in range(4)]

    def answer(self, expression):
        if expression == "pass":
            self.nums = self.get_my_cards()
            return False

        counts = [0] * 10
        for c in expression:
            if c.isdigit():
                counts[int(c)] += 1

        for num in self.nums:
            if counts[num] > 0:
                counts[num] -= 1
            else:
                return False

        if any(count != 0 for count in counts):
            return False

        return self.evaluate_expression(expression)

    def evaluate_expression(self, expression):
        pos = -1
        ch = None

        def next_char():
            nonlocal pos, ch
            pos += 1
            ch = expression[pos] if pos < len(expression) else None

        def eat(char_to_eat):
            while ch == ' ':
                next_char()
            if ch == char_to_eat:
                next_char()
                return True
            return False

        def parse_expression():
            x = parse_term()
            while True:
                if eat('+'):
                    x += parse_term()
                elif eat('-'):
                    x -= parse_term()
                else:
                    return x

        def parse_term():
            x = parse_factor()
            while True:
                if eat('*'):
                    x *= parse_factor()
                elif eat('/'):
                    x /= parse_factor()
                else:
                    return x

        def parse_factor():
            nonlocal pos
            if eat('+'):
                return parse_factor()
            if eat('-'):
                return -parse_factor()

            x = 0.0
            start_pos = pos
            if eat('('):
                x = parse_expression()
                eat(')')
            elif (ch is not None and '0' <= ch <= '9') or ch == '.':
                while (ch is not None and '0' <= ch <= '9') or ch == '.':
                    next_char()
                x = float(expression[start_pos:pos])
            else:
                raise ValueError("Unexpected: " + str(ch))

            return x

        def parse():
            next_char()
            x = parse_expression()
            if pos < len(expression):
                raise ValueError("Unexpected: " + str(ch))
            return x

        try:
            return parse() == 24
        except Exception:
            return False

    def get_nums(self):
        return self.nums