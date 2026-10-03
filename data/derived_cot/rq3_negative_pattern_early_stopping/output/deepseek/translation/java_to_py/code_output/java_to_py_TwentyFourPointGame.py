import random

class TwentyFourPointGame:
    def __init__(self):
        self.nums = self._get_my_cards()

    def _get_my_cards(self):
        return [random.randint(1, 9) for _ in range(4)]

    def answer(self, expression):
        if expression == "pass":
            self.nums = self._get_my_cards()
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

        return self._evaluate_expression(expression)

    def _evaluate_expression(self, expression):
        try:
            pos = -1
            ch = ''

            def next_char():
                nonlocal pos, ch
                pos += 1
                if pos < len(expression):
                    ch = expression[pos]
                else:
                    ch = ''

            def eat(char_to_eat):
                nonlocal ch
                while ch == ' ':
                    next_char()
                if ch == char_to_eat:
                    next_char()
                    return True
                return False

            def parse():
                next_char()
                x = parse_expression()
                if pos < len(expression):
                    raise RuntimeError("Unexpected: " + ch)
                return x

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
                if eat('+'):
                    return parse_factor()
                if eat('-'):
                    return -parse_factor()

                start_pos = pos
                if eat('('):
                    x = parse_expression()
                    eat(')')
                    return x
                elif ch.isdigit() or ch == '.':
                    while ch.isdigit() or ch == '.':
                        next_char()
                    x = float(expression[start_pos:pos])
                    return x
                else:
                    raise RuntimeError("Unexpected: " + ch)

            result = parse()
            return result == 24.0
        except Exception:
            return False

    def get_nums(self):
        return self.nums