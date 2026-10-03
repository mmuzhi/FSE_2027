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

        for count in counts:
            if count != 0:
                return False

        return self.evaluateExpression(expression)

    def evaluateExpression(self, expression):
        try:
            pos = [-1]
            ch = [-1]

            def next_char():
                pos[0] += 1
                ch[0] = ord(expression[pos[0]]) if pos[0] < len(expression) else -1

            def eat(char_to_eat):
                while ch[0] == ord(' '):
                    next_char()
                if ch[0] == char_to_eat:
                    next_char()
                    return True
                return False

            def parse():
                next_char()
                x = parse_expression()
                if pos[0] < len(expression):
                    raise RuntimeError("Unexpected: " + chr(ch[0]))
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

            def parse_term():
                x = parse_factor()
                while True:
                    if eat(ord('*')):
                        x *= parse_factor()
                    elif eat(ord('/')):
                        x /= parse_factor()
                    else:
                        return x

            def parse_factor():
                if eat(ord('+')):
                    return parse_factor()
                if eat(ord('-')):
                    return -parse_factor()

                x = 0.0
                start_pos = pos[0]
                if eat(ord('(')):
                    x = parse_expression()
                    eat(ord(')'))
                elif (ord('0') <= ch[0] <= ord('9')) or ch[0] == ord('.'):
                    while (ord('0') <= ch[0] <= ord('9')) or ch[0] == ord('.'):
                        next_char()
                    x = float(expression[start_pos:pos[0]])
                else:
                    raise RuntimeError("Unexpected: " + chr(ch[0]))

                return x

            return parse() == 24
        except Exception:
            return False

    def getNums(self):
        return self.nums