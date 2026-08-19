import math
import random
import time


def _c_div(x, y):
    # Emulates C++ double division: division by zero yields inf/nan instead of raising.
    if y == 0:
        if x == 0:
            return float('nan')
        return float('inf') if x > 0 else float('-inf')
    return x / y


def _c_pow(x, y):
    # Emulates std::pow edge cases: overflow -> inf, domain error -> nan (pole error -> inf).
    try:
        return math.pow(x, y)
    except OverflowError:
        return float('inf')
    except ValueError:
        if x == 0.0:
            return float('inf')
        return float('nan')


class TwentyFourPointGame:
    def __init__(self):
        self.nums = []
        random.seed(time.time())

    def generate_cards(self):
        for _ in range(4):
            self.nums.append(random.randint(1, 9))
        assert len(self.nums) == 4

    def get_my_cards(self):
        self.nums.clear()
        self.generate_cards()
        return list(self.nums)

    def answer(self, expression):
        if expression == "pass":
            return self.get_my_cards()

        statistic = {}
        for c in expression:
            if '0' <= c <= '9' and int(c) in self.nums:
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
            '/': _c_div,
            '^': _c_pow,
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
                    operand_stack.append(float(num_buffer))
                    num_buffer = ''

                if ch in ('+', '-', '*', '/', '^'):
                    while (operator_stack and operator_stack[-1] != '('
                           and self.precedence(operator_stack[-1]) >= self.precedence(ch)):
                        operand_stack, operator_stack = self.apply_operator(operand_stack, operator_stack)
                    operator_stack.append(ch)
                elif ch == '(':
                    operator_stack.append(ch)
                elif ch == ')':
                    while operator_stack and operator_stack[-1] != '(':
                        operand_stack, operator_stack = self.apply_operator(operand_stack, operator_stack)
                    operator_stack.pop()

        if num_buffer:
            operand_stack.append(float(num_buffer))

        while operator_stack:
            operand_stack, operator_stack = self.apply_operator(operand_stack, operator_stack)

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