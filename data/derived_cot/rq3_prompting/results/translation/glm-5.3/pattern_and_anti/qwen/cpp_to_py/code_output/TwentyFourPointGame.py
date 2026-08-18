import math
import random
import re


def _stod(s):
    # Mimics std::stod for buffers containing only digits/dots: parses the
    # longest valid numeric prefix, raises ValueError if there is none.
    m = re.match(r'(?:\d+(?:\.\d*)?|\.\d+)', s)
    if m is None:
        raise ValueError("stod: no conversion")
    return float(m.group())


def _divide(x, y):
    # IEEE-754 style division: never raises on zero divisor (C++ double semantics).
    if y != 0:
        return x / y
    if x == 0:
        return float('nan')
    return float('inf') if x > 0 else float('-inf')


class TwentyFourPointGame:
    def __init__(self):
        self.nums = []
        random.seed()

    def generate_cards(self):
        for _ in range(4):
            self.nums.append(random.randint(1, 9))
        assert len(self.nums) == 4

    def get_my_cards(self):
        self.nums.clear()
        self.generate_cards()
        return self.nums

    def answer(self, expression):
        if expression == "pass":
            return self.get_my_cards()

        statistic = {}
        for c in expression:
            if '0' <= c <= '9' and (ord(c) - ord('0')) in self.nums:
                statistic[c] = statistic.get(c, 0) + 1

        nums_used = dict(statistic)

        for num in self.nums:
            key = chr(ord('0') + num)
            if key in nums_used and nums_used[key] > 0:
                nums_used[key] -= 1
            else:
                return []

        if all(v == 0 for v in nums_used.values()):
            if self.evaluate_expression(expression):
                return [1]
            else:
                return []
        else:
            return []

    def evaluate_expression(self, expression):
        try:
            if expression[0] < '0' or expression[0] > '9':
                if expression[0] != '(':
                    raise ValueError
            kkk = len(expression) - 1
            if expression[kkk] < '0' or expression[kkk] > '9':
                if expression[kkk] != ')':
                    raise ValueError
            calculator = Calculator()
            ans = calculator.calculate(expression)
            return ans == 24.0
        except Exception:
            return False

    def set_nums(self, now):
        self.nums = list(now)


class Calculator:
    def __init__(self):
        self.operators = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: x - y,
            '*': lambda x, y: x * y,
            '/': _divide,
            '^': lambda x, y: math.pow(x, y),
        }

    def calculate(self, expression):
        if not expression:
            return 0.0

        operand_stack = []
        operator_stack = []
        num_buffer = ''

        for ch in expression:
            if ('0' <= ch <= '9') or ch == '.':
                num_buffer += ch
            else:
                if num_buffer:
                    operand_stack.append(_stod(num_buffer))
                    num_buffer = ''

                if ch in ('+', '-', '*', '/', '^'):
                    while (operator_stack and operator_stack[-1] != '('
                           and self.precedence(operator_stack[-1]) >= self.precedence(ch)):
                        self.apply_operator(operand_stack, operator_stack)
                    operator_stack.append(ch)
                elif ch == '(':
                    operator_stack.append(ch)
                elif ch == ')':
                    while operator_stack and operator_stack[-1] != '(':
                        self.apply_operator(operand_stack, operator_stack)
                    operator_stack.pop()

        if num_buffer:
            operand_stack.append(_stod(num_buffer))

        while operator_stack:
            self.apply_operator(operand_stack, operator_stack)

        return operand_stack[-1] if operand_stack else 0.0

    def precedence(self, op):
        if op in ('+', '-'):
            return 1
        if op in ('*', '/'):
            return 2
        if op == '^':
            return 3
        return 0

    def apply_operator(self, operand_stack, operator_stack):
        op = operator_stack.pop()

        operand2 = operand_stack.pop()
        operand1 = operand_stack.pop()

        result = self.operators[op](operand1, operand2)
        operand_stack.append(result)

        return operand_stack, operator_stack